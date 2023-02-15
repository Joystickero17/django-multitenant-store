from itertools import product
from operator import xor
from pprint import pprint
import uuid
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import views
from rest_framework import permissions, exceptions
from rest_framework import pagination
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework import response
from django.db.models.query_utils import Q
from django.db.models import Max, Sum,Min,Count,Value,F
from django.db.models.functions import Greatest,Least,Coalesce
from core.controllers import order_controller
from core.controllers.notification_controller import create_notification
from core.models import Store, Products
from core.models.cart import Cart
from core.models.chat.message import Message
from core.models.external_payments import ExternalPayment
from core.models.media import Media
from core.models.order import Order
from core.models.product_order import CartItem, ProductOrder
from core.models.user_data.address import Address
from core.models.user_payment import UserPayment
from core.models.wishlist import Wish
from core.models.assistance import Assistance
from core.models.export_file import ExportFile
from core.models.gc_model import GiftCard
from core.permissions.store_owner_permissions import WebSiteOperatorPermission
from core.permissions.wish_permission import SameUserPermission
from core.serializers.assistance_serializer import AssistanceSerializer
from core.serializers.brand_serializer import BrandSerializer, Brand
from core.serializers.cart_item_serializer import CartItemSerializer
from core.serializers.category_serializer import CategorySerializer, Category
from core.serializers.chat_serializer import ChatMessageSerializer, UserChatMessageSerializer
from core.serializers.export_file_serializer import ExportFileSerializer
from core.serializers.external_payment_serializer import ExternalPaymentSerializer
from core.serializers.order_serializer import OrderSerializer, StoreOrderSerializer
from core.serializers.pago_movil_serializer import PagoMovilSerializer
from core.serializers.payment_serializer import PaymentSerializer
from core.serializers.product_order_serializer import ProductOrderSerializer
from core.serializers.product_serializer import ProductSerializer
from core.serializers.query_param_serializer import QueryParamSerializer
from core.serializers.store_serializer import StoreSerializer
from core.serializers.user_config_serializer import UserConfigSerializer
from core.serializers.review_serializer import ReviewSerializer, Review
from core.serializers.user_payment_serializer import UserPaymentSerializer
from core.serializers.wish_serializer import WishSerializer
from core.serializers.user_register_serializer import UserRegisterSerializer
from core.serializers.chart_serializers import HistoricSalesSerializer
from core.serializers.image_serializer import ImageSerializer
from core.serializers.invited_user_serializer import InvitedUserSerializer
from core.serializers.manual_order_paid_serializer import ManualMarkOrderSerializer
from core.utils.model_choices import PaymentMethodChoices,OrderStatusChoices, UserTypeRegisterChoices
from .permissions.tenant_permission import TenantPermission
from core.controllers.coinbase_controller import create_charge
from django.contrib.auth import get_user_model
from cities_light.contrib.restframework3 import RegionModelViewSet, SubRegionModelViewSet,CityModelViewSet
from core.controllers import paypal_controller
from core.controllers import chart_controller
from core.choices.model_choices import RoleChoices, SendgridTemplateChoices
from django.contrib.auth.models import Permission,Group
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from core.tasks import export_contacts, export_orders, export_products, generate_profile_pic,generate_store_pic,send_email_template_task, export_chart,export_assistances
from core.models.notificacions import Notification
from core.serializers.notification_serializer import NotificationSerializer
from core.serializers.order_serializer import PrivateUserSerializer
from core.serializers.product_storage_serializer import ProductStorageSerializer,ProductStorage
from ip_logger.models import IPAddress
channel_layer = get_channel_layer()

User = get_user_model()

def store_context_view(request):
    data = {}
    if not request.user.is_authenticated:
        data["wish_list"] = []
        return data
    if not hasattr(request.user, "cart"):
        Cart.objects.create(user=request.user)
    return data

class ExportFileView(ModelViewSet):
    serializer_class = ExportFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ExportFile.objects.all()
    


class ProductStorageView(ModelViewSet):
    serializer_class = ProductStorageSerializer
    queryset = ProductStorage.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = [
        "region",
        "subregion",
        "city",
        "store__name"
    ]
    

    def get_queryset(self):
        queryset = super().get_queryset()
        store_storage_only = self.request.query_params.get("store_storage_only","").lower() == "true" or self.request.user.role != RoleChoices.WEBSITE_OWNER
        if not store_storage_only:
            return queryset
        return queryset.filter(store=self.request.user.store)

class UserPaymentView(ModelViewSet):
    serializer_class = UserPaymentSerializer
    queryset = UserPayment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        store_payments_only = self.request.query_params.get("store_payments_only","").lower() == "true" or self.request.user.role != RoleChoices.WEBSITE_OWNER
        queryset = super().get_queryset()
        if not store_payments_only:
            return queryset
        return queryset.filter(user=self.request.user)

class ManualMarkOrderPaid(views.APIView):
    """
    EP para marcar una orden pagada manualmente, si se trata de un pago movil o una
    transferencia bancaria cuya integracion con el sistema no exista
    """
    permission_classes = [WebSiteOperatorPermission]

    def post(self, request , *args, **kwargs):
        serializer = ManualMarkOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        is_paid = data["is_paid"]
        order = data["order"]
        if not is_paid:
            return response.Response({"message":f"No se ejecutaron cambios en la Orden {order.pk}"})
        if not (order.external_payments.exists() or order.external_payment_id):
            raise exceptions.ValidationError({"message":"La order no tiene, ni external payment id, asi como tampoco pagos anexos registrados, no se puede marcar como pagada"})
        order_controller.on_payment_aprove(order)
        return response.Response({"message":"Orden actualizada con éxito"})
        

class SendGiftCardView(views.APIView):
    """
    Vista para enviar una Gift Card
    """
    def post(self, request, *args, **kwargs):
        gc = GiftCard.objects.filter(user__isnull=True).first()
        if not gc:
            raise exceptions.ValidationError({"message": "No hay Gift Cards disponibles, por favor intenta mas tarde"})
        if request.user.credits < 5000:
            raise exceptions.ValidationError({"message": "Debe tener al menos 5000 puntos para retirar una Gift Card"})
        request.user.credits -= 5000
        request.user.save()
        send_email_template_task.delay(
            [request.user.email],
            SendgridTemplateChoices.GC_AMAZON,
            {
                "name": request.user.email or request.user.email,
                "code": gc.code
            }
        )
        return response.Response({"message": "Codigo enviado con éxito!"})



class FreelanceAssistance(ModelViewSet):
    queryset = Assistance.objects.all()
    serializer_class = AssistanceSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "freelance__first_name",
        "freelance__last_name",
        "freelance__email",
    ]
    def get_queryset(self):
        queryset = super().get_queryset()
        states = self.request.query_params.getlist("states[]",[])
        feedback = self.request.query_params.getlist("feedback[]",[])
        states = [state=='true' for state in states if (state == 'true') in [True,False]]
        feedback = [fb =='true' for fb in feedback if (fb == 'true' )in [True,False]]
        if states:
            queryset = queryset.filter(completed__in=states)
        if feedback:
            queryset = queryset.filter(feedback__in=feedback)
        return queryset

class FreelanceStatsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # pprint(
        #     User.objects.filter(role=RoleChoices.FREELANCE).annotate(asist_count=Count("assistances")).order_by("-asist_count").values("email","asist_count"),
        # )
        # pprint(User.objects.all().annotate(asist_count=Count("customer_assistances",filter=Q(customer_assistances__feedback=True))).order_by("-asist_count").values("email","asist_count"))
        current_store_stats = request.query_params.get("current_store_stats") == "true" or request.user.role == RoleChoices.WEBSITE_OWNER
        best_freelance = User.objects.filter(role=RoleChoices.FREELANCE).annotate(asist_count=Count("assistances")).order_by("-asist_count").first()
        most_assisted_customer = User.objects.annotate(asist_count=Count("customer_assistances",filter=Q(customer_assistances__feedback=True))).order_by("-asist_count").first()
        p_o = ProductOrder.objects.filter(
            assistance__isnull=False
            )
        c_i = CartItem.objects.filter(assistance__isnull=False)
        if current_store_stats:
            p_o = p_o.filter(product__store=request.user.store)
            c_i = c_i.filter(product__store=request.user.store)
        current_store_assist_received = p_o.values(
            "product",
            "assistance",
            "quantity",
            "created_at",
            "updated_at",
            ).union(c_i.values(
            "product",
            "assistance",
            "quantity",
            "created_at",
            "updated_at",
            )).count()
        return response.Response({
            "best_freelance": PrivateUserSerializer(best_freelance).data,            
            "most_assisted_customer":PrivateUserSerializer(most_assisted_customer).data,
            "assist_received":current_store_assist_received
            }
        )

class AssistanceMessages(views.APIView):
    def post(self, request, *args, **kwargs):
        a_id = request.data.get("a_id")
        if not a_id:
            raise exceptions.ValidationError("debe proporcionar el id de la asistencia")
        if not a_id.isdigit():
            raise exceptions.ValidationError("Id debe ser un numero válido")
        
        assistance= get_object_or_404(Assistance, pk=a_id)
        messages = Message.objects.filter(
            Q(from_user=request.user) &
            Q(to_user=assistance.freelance) |
            Q(from_user=assistance.freelance) &
            Q(to_user=request.user)
            ).order_by("created_at")
        serializer = ChatMessageSerializer(messages, many=True)
        return response.Response(serializer.data)

class UserChatViewSet(ModelViewSet):
    serializer_class = UserChatMessageSerializer
    queryset = User.objects.all()
    http_methods = ["get"]

    def get_queryset(self):
        messages = Message.objects.filter(to_user=self.request.user).values_list("from_user__id", flat=True)
        queryset = super().get_queryset().annotate(
                message_date=Min("sent_messages__created_at", filter=Q(sent_messages__to_user=self.request.user)&~Q(sent_messages__from_user=self.request.user)),
                message_count=Count("received_messages")
                ).order_by(F("message_date").desc(nulls_last=True))
        pprint(list(queryset.values("id","message_count", "email","message_date")))
        return queryset

class ChatViewSet(ModelViewSet):
    serializer_class = ChatMessageSerializer
    queryset = Message.objects.all()

    


class ContactViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PrivateUserSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "email"
    ]
    http_methods = ["get"]
    def get_queryset(self):
        queryset = super().get_queryset().annotate(sale_count=Count(
            "order",
            filter=Q(order__payment_status=OrderStatusChoices.PAYMENT_SUCCESS)
            )).order_by("-sale_count")
        store_contacts_only = self.request.query_params.get("store_contacts_only","").lower() == "true" or self.request.user.role != RoleChoices.WEBSITE_OWNER
        user_ids = Order.objects.filter(product_orders__product__store=self.request.user.store).values_list("user__id",flat=True)
        if not store_contacts_only:
            user_ids = Order.objects.values_list("user__id",flat=True)
        queryset = queryset.filter(id__in=user_ids)
        return queryset.filter(id__in=user_ids)


class NotificationView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated or self.request.user.role == 'freelance':
            return super().get_queryset().filter(channel_group__name="public")
        return super().get_queryset().filter(channel_group__name=f"store_{self.request.user.store.slug}")

class MediaViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Media.objects.all()
    


class CustomSubRegionView(SubRegionModelViewSet):
    def get_queryset(self):
        queryset =  super().get_queryset()
        region = self.request.query_params.get("region")
        if region:
            queryset = queryset.filter(region__name_ascii=region)
        return queryset

class CustomCityView(CityModelViewSet):
    def get_queryset(self):
        queryset =  super().get_queryset()
        region = self.request.query_params.get("subregion")
        if region:
            queryset = queryset.filter(subregion__name_ascii=region)
        return queryset

class PageNumberPaginationWithCount(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        response = super(PageNumberPaginationWithCount, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['current_page'] = self.page.number
        return response


class SmallPagination(PageNumberPaginationWithCount):
    page_size = 5


class StoreTenantViewset(ModelViewSet):
    pagination_class = PageNumberPaginationWithCount

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not hasattr(self.request.user, "store"):
            return context
        return {**context, "store":self.request.user.store}


class UserInfoView(views.APIView):
    permission_classes = [SameUserPermission]

    def get(self, request, *args, **kwargs):
        return response.Response({"name":request.user.first_name,"last_name":request.user.last_name})


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        return queryset.filter(cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, "cart"):
           request.user.cart = Cart(user=self.request.user)
           request.user.cart.save()
           request.user.save()
        new_data = request.data.copy()
        new_data["cart"] = request.user.cart.id
        serializer = self.serializer_class(data=new_data)
        serializer.is_valid(raise_exception=True)
        order = CartItem.objects.filter(cart=request.user.cart, product=serializer.validated_data.get("product")).first()
        if not order:
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        order.delete()
        return response.Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        if not hasattr(request.user, "cart"):
            Cart.objects.create(user=request.user)
            
        print(request.user.cart.total_order)
        data["total_cart"] = request.user.cart.total_order
        return response.Response(data)

class StoreViewSet(StoreTenantViewset):
    queryset = Store.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    serializer_class = StoreSerializer


class WishListViewset(ModelViewSet):
    serializer_class = WishSerializer
    permission_classes = [SameUserPermission]
    queryset = Wish.objects.all()

    def perform_create(self, serializer):
        exists = Wish.objects.filter(user=self.request.user, product=serializer.validated_data.get("product")).first()
        if exists: raise exceptions.ValidationError("Este producto ya existe en tu lista de deseos")
        return serializer.save(user=self.request.user)
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
class ReviewViewSet(StoreTenantViewset):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
    pagination_class = SmallPagination

    def perform_create(self, serializer):
        product = product=serializer.validated_data["product"]
        orders = self.request.user.order_set.filter(product_orders__product=product)
        print(orders)
        if not orders.exists(): raise exceptions.ValidationError("Para hacer un Review debes efectuar una compra primero")
        review = Review.objects.filter(user=self.request.user, product=product)
        print(self.request.user, serializer.validated_data.get("product").id)
        print(review.values())
        if review.exists(): raise exceptions.ValidationError("Ya has hecho una review para este producto no puedes hacer más")
        return serializer.save(user=self.request.user)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        product = params.get("product")
        
        if not product:
            return queryset
        if product.isdigit():
            queryset = queryset.filter(product__id=product)

        return queryset

class MaxPriceProduct(views.APIView):
    def get(self, request, *args, **kwargs):
        max_price = Products.objects.all().aggregate(max_price=Max("price")).get('max_price')
        return response.Response({"max_price": max_price})

class ProductViewSet(StoreTenantViewset):
    """
    Uso Publico en lectura
    """
    permission_classes = [TenantPermission]
    queryset = Products.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name","price"]
    serializer_class = ProductSerializer
    pagination_class = PageNumberPaginationWithCount

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        serializer = QueryParamSerializer(data=params)
        data_is_valid = serializer.is_valid()
        validated_params = serializer.validated_data
        max_price = validated_params.get("max_price")
        min_price = validated_params.get("min_price")
        free_products = validated_params.get("free_products")
        slug = params.get("slug_store")
        brands = params.getlist("brand[]")
        
        
        if brands:
            queryset = queryset.filter(brand__name__in=brands)
        if slug:
            queryset = queryset.filter(store__slug=slug)
        if all([max_price, min_price]):
            # BUG REPEATED WHERE queryset2 = queryset.filter(Q(price__isnull=True) | (Q(price__gte=min_price) & Q(price__lte=max_price)))
            q_objects = Q(price__gte=min_price) & Q(price__lte=max_price) | Q(price=None) if free_products else Q(price__gte=min_price) & Q(price__lte=max_price)
            return queryset.filter(q_objects)
        if min_price:
            return queryset.filter(Q(price__gte=min_price) | Q(price__isnull=bool(free_products)))
        if max_price:
            return queryset.filter(Q(price__lte=max_price) | Q(price__isnull=bool(free_products)))
        if params.get("o") == "popular":
            queryset = queryset.order_by("-reviews__count")

        return queryset

class PrivateStoreProductViewSet(ProductViewSet):
    def get_queryset(self):
        params = self.request.query_params
        products_store_only = params.get("products_store_only") == 'true'
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        queryset = super().get_queryset()
        if not self.request.user.role == RoleChoices.WEBSITE_OWNER or products_store_only:
            queryset = queryset.filter(store=self.request.user.store)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

class MostSoldProductView(views.APIView):
    def get(self, request, *args, **kwargs):
        queryset = Products.objects.order_by("product_orders")[:5]
        return response.Response(ProductSerializer(queryset, many=True).data)


class UserConfigView(StoreTenantViewset):
    serializer_class = UserConfigSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

class CategoryViewset(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    queryset = Category.objects.all()

    def filter_queryset(self, queryset):
        parents_only = self.request.query_params.get("parents_only","").lower() == "true"
        parent = self.request.query_params.get("parent")
        if parents_only:
            queryset = queryset.filter(parent=None)
        if parent:
            if parent.isdigit():
                queryset = queryset.filter(parent=parent)
        return super().filter_queryset(queryset)

class BrandViewset(ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    queryset = Brand.objects.all()

class ProductOrderView(ModelViewSet):
    serializer_class = ProductOrderSerializer
    queryset = ProductOrder.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["product__name"]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order = self.request.query_params.get("order")
        queryset = super().get_queryset()
        if order:
            return queryset.filter(order__id=order)
        return queryset

class AdminCreateInvitedUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = InvitedUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        password = User.objects.make_random_password()
        user_exists = User.objects.filter(email=data["email"]).exists()
        if user_exists:
            raise exceptions.ValidationError({"message":"El usuario ya existe por favor, comuniquese con soporte para asignárselo a su tienda"})
        
        user = User.objects.create_user(email=data["email"], password=password)
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.phone_number = data.get("phone_number")
        user.store = request.user.store
        user.role = RoleChoices.STORE_OPERATOR
        user.save()
        generate_profile_pic.delay(user.email)
        send_email_template_task.delay([user.email], SendgridTemplateChoices.BIENVENIDO_INVITADO,{"name": user.first_name, "password":password, "from":request.user.email})
        return response.Response(serializer.data)


class StoreUsersView(ModelViewSet):
    serializer_class = UserConfigSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        queryset = super().get_queryset()
        store_users_only = self.request.query_params.get("store_users_only") == "true"

        if self.request.user.role != RoleChoices.WEBSITE_OWNER or store_users_only:
            return queryset.filter(store=self.request.user.store)

        return queryset

class ClientOrderViewSet(ModelViewSet):
    """
    Endpoint para ordenes de clientes
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    filter_backends = [SearchFilter]
    pagination_class = SmallPagination
    search_fields = ["product_orders__product__name"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
        
class OrderViewSet(ModelViewSet):
    """
    Endpoint para ordenes de clientes
    """
    serializer_class = StoreOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    filter_backends = [SearchFilter]
    pagination_class = SmallPagination
    search_fields = [
        'id',
        "product_orders__product__name",
        "payment_method",
                ]

    def get_queryset(self):
        queryset = super().get_queryset()
        store_orders_only = self.request.query_params.get("store_orders_only") == "true"

        if self.request.user.role != RoleChoices.WEBSITE_OWNER or store_orders_only:
            queryset = super().get_queryset().filter(product_orders__product__store=self.request.user.store).distinct()
        
        params = self.request.query_params
        status = params.getlist("status[]")
        print(status)
        if status:
            queryset = queryset.filter(payment_status__in=status)
        return queryset

class CoinbaseWebHookView(views.APIView):
    """
    Endpoint para recibir notificaciones de pago de Coinbase
    """
    def post(self, request, *args, **kwargs):
        pass

class PaypalCaptureOrder(views.APIView):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get("paypal_order_id")
        if not order_id:
            raise exceptions.ValidationError("Debe incluir el id de la orden de paypal para el capture")
        res : dict = paypal_controller.capture_order(order_id)
        print(res)
        paypal_order_id = res.get("id")
        if res.get("status") == "COMPLETED":
            order = Order.objects.filter(external_payment_id=paypal_order_id).first()
            order_controller.on_payment_aprove(order)
            return response.Response({**res, "redirect_to":reverse("order_detail", kwargs={'pk':order.id})})
        return response.Response(res)


class PaymentView(ViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        total_order = request.user.cart.total_order
        if not total_order:
            request.data["payment_type"] = PaymentMethodChoices.FREE_ITEM
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print(data)
        payment_type = data.get("payment_type")
        aditional_info = data.get("aditional_info")
        save_billing_info = data.get("save_billing_info")
        user_address = data.get("user_address")
        region, subregion, city = data.get("region"), data.get("subregion"), data.get("city")
        short_address = data.get("short_address")
        order_address = None
        if not hasattr(request.user, "cart"):
            raise exceptions.ValidationError({"message":"Usuario no tiene carrito de compras creado"})
        
        print(request.user.cart.cart_items.all())

        if not request.user.cart.cart_items.exists():
            raise exceptions.ValidationError({"message":"El carrito esta vacio"})
        
        print(user_address)

        if user_address:
            order_address = user_address
        elif save_billing_info:
            # desactiva las existentes como principales
            if request.user.addresses.count() > 0:
                request.user.addresses.all().update(is_main=False)
            
            # guarda la informacion y la hace principal
            order_address = Address.objects.create(
                name=data.get("name"),
                last_name=data.get("last_name"),
                user=request.user,
                is_main=True,
                region=region,
                subregion=subregion,
                short_address=short_address,
                city=city
            )
        total_amount = request.user.cart.total_order
        order_id = order_controller.create_order_from_cart(request.user.cart, payment_type, address=order_address)
        # print(total_amount)
        order_id.aditional_info = aditional_info
        order_id.save()
        if total_amount == 0:
            # Caso donde la compra es gratuita
            # TODO: link para redireccion a orden cerrada
            order_id.payment_status = OrderStatusChoices.PAYMENT_SUCCESS
            order_id.payment_method = PaymentMethodChoices.FREE_ITEM
            order_id.external_payment_id = f"FREEITEM{uuid.uuid4()}"
            order = order_controller.on_payment_aprove(order_id)
            res = {
                "href":reverse("order_detail"),
                "order": order.id
            }
            return response.Response(res) 
        
        if payment_type == PaymentMethodChoices.PAYPAL:
            # Caso Paypal
            all_product_orders = order_id.product_orders.all()
            items = [{
                        "name": item.product.name,
                        "description": "The best item ever",
                        "unit_amount": {
                            "currency_code": "USD",
                            "value": str(item.quantity*item.product.price)
                        },
                        "quantity": item.quantity
                    } for item in all_product_orders]
            res = paypal_controller.create_order(items, order=order_id)
            order_id.external_payment_id = res.get("id")
            order_id.save()
            return response.Response(res)
        if payment_type == PaymentMethodChoices.PAGO_MOVIL:
            
            res = {
                "href":reverse("order_detail"),
                "order": order_id.id

            }
            return response.Response(res, status=status.HTTP_202_ACCEPTED)

        # caso Coinbase
        res : dict = create_charge(request.user.full_name, "descripcion de prueba", total_amount , order_id.pk)
        if not res: raise exceptions.ValidationError({
            "message":"A ocurrido un error con la pasarela de pago, no se obtuvo respuesta desde el servidor"
            })
        return response.Response(res, status=status.HTTP_202_ACCEPTED)


class UserRegisterViewSet(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        initial_data = serializer.initial_data
        data = serializer.validated_data
        user_type = data.get("user_type")
        
        # TODO: send verification email
        user = User.objects.create_user(
            email=data.get("email"),
            password=data.get("password"),
            is_active=True # TODO: verificar correo
            )
        user.phone_number = data.get("phone_number")
        user.first_name = data.get("name")
        user.last_name = data.get("last_name")
        user.save()
        Cart.objects.create(user=user)
        if user_type == UserTypeRegisterChoices.FREELANCE:
            # TODO: create Freelance Info
            user.role = UserTypeRegisterChoices.FREELANCE
            user.save()

        if user_type == UserTypeRegisterChoices.SHOP:
            # TODO: Store Info
            data_store = {
                "name": initial_data.get("company_name"),
                "bussiness_legal_id": initial_data.get("rif"),
                "company_employee_number": initial_data.get("company_employee_number"),
                "company_anual_income": initial_data.get("company_anual_income"),
                "category": initial_data.get("company_main_category"),
            }
            store_serializer = StoreSerializer(data=data_store)
            store_serializer.is_valid(raise_exception=True)
            store_instance = store_serializer.save()
            user.store = store_instance
            user.role = RoleChoices.STORE_OWNER
            user.groups.add(Group.objects.get(name=RoleChoices.STORE_OWNER))
            user.save()
            generate_store_pic.delay(store_instance.id)

        if user_type == UserTypeRegisterChoices.CUSTOMER:
            user.role = UserTypeRegisterChoices.CUSTOMER
            user.save()
            #TODO: send welcome email
            

        generate_profile_pic.delay(user.email)
        return response.Response(status=status.HTTP_201_CREATED)

class SelfUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes =  [ permissions.IsAuthenticated]
    serializer_class = UserConfigSerializer
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

class TestWebSocketView(views.APIView):
    def get(self, request, *args, **kwargs):
        group = request.user.email.replace("@","_").replace(".","_")
        create_notification(
        content="Notification de Ahora", 
        entity_name="order", 
        entity_id=None, 
        group="store_mls-parts-ca"
        )
        return response.Response()


class ExternalPaymentViewsSet(ModelViewSet):
    serializer_class = ExternalPaymentSerializer
    queryset = ExternalPayment.objects.all()
        


class HistoricSalesView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = HistoricSalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        current_store_stats = data["store_stats_only"] or request.user.role != RoleChoices.WEBSITE_OWNER
        print(current_store_stats)
        chart_data = chart_controller.current_store_controller(
            request.user.store, 
            data["chart_type"],
            year=data["year"],
            month=data.get("month"),
            current_store_stats=current_store_stats
             )
        total_sales_count = chart_controller.total_sales_count(
            request.user.store,
            current_store_stats=current_store_stats
            )
        total_review_count = chart_controller.total_review_count(
            request.user.store,
            current_store_stats=current_store_stats
            )
        global_store_product_count =  request.user.role == RoleChoices.WEBSITE_OWNER and not current_store_stats
        product_count = request.user.store.products.all().count()
        user_count = request.user.store.user_set.all().count()
        if global_store_product_count:
            product_count = Products.objects.all().count() 
            user_count = User.objects.all().count()
        print(product_count)
        print(total_sales_count)
        return response.Response({
            "chart":chart_data,
            "total_sales_count":total_sales_count,
            "total_freelancers":chart_controller.get_total_freelancers(),
            "refunds":0,
            "visits": IPAddress.objects.all().count(),
            "products":product_count,
            "users":user_count,
            "reviews":total_review_count
            })

class HistoricSalesViewExport(HistoricSalesView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        yearly = request.data.get("yearly", "").lower() == "true"
        print(res.data)
        export_chart.delay(res.data,yearly,request.user.email)
        return response.Response({"message":"Ha comenzado una nueva exportación con éxito"})
class ContactViewSetExport(ContactViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        ids = list(queryset.values_list("id", flat=True))
        export_contacts.delay(ids, self.request.user.email)
        return queryset
    
class OrderViewSetExport(OrderViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        ids = list(queryset.values_list("id", flat=True))
        export_orders.delay(ids, self.request.user.email)
        return queryset
    

class FreelanceAssistanceExport(FreelanceAssistance):
    def get_queryset(self):
        queryset = super().get_queryset()
        ids = list(queryset.values_list("id", flat=True))
        export_assistances.delay(ids, self.request.user.email)
        return queryset

class PrivateStoreProductExport(PrivateStoreProductViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        ids = list(queryset.values_list("id", flat=True))
        export_products.delay(ids, self.request.user.email)
        return queryset