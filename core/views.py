from itertools import product
from operator import xor
import uuid
from django.shortcuts import render
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import views
from rest_framework import permissions, exceptions
from rest_framework import pagination
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework import response
from django.db.models.query_utils import Q
from django.db.models import Max, Sum
from core.controllers import order_controller
from core.models import Store, Products
from core.models.cart import Cart
from core.models.order import Order
from core.models.product_order import CartItem, ProductOrder
from core.models.user_data.address import Address
from core.models.wishlist import Wish
from core.permissions.wish_permission import SameUserPermission
from core.serializers.brand_serializer import BrandSerializer, Brand
from core.serializers.cart_item_serializer import CartItemSerializer
from core.serializers.category_serializer import CategorySerializer, Category
from core.serializers.order_serializer import OrderSerializer
from core.serializers.payment_serializer import PaymentSerializer
from core.serializers.product_order_serializer import ProductOrderSerializer
from core.serializers.product_serializer import ProductSerializer
from core.serializers.query_param_serializer import QueryParamSerializer
from core.serializers.store_serializer import StoreSerializer
from core.serializers.user_config_serializer import UserConfigSerializer
from core.serializers.review_serializer import ReviewSerializer, Review
from core.serializers.wish_serializer import WishSerializer
from core.utils.model_choices import PaymentMethodChoices,OrderStatusChoices
from .permissions.tenant_permission import TenantPermission
from core.controllers.coinbase_controller import create_charge
from django.contrib.auth import get_user_model
from cities_light.contrib.restframework3 import RegionModelViewSet, SubRegionModelViewSet,CityModelViewSet
from core.controllers import paypal_controller

User = get_user_model()

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
        review = Review.objects.filter(user=self.request.user, product=serializer.validated_data.get("product"))
        if review: raise exceptions.ValidationError("Ya has hecho una review para este producto no puedes hacer más")
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
    permission_classes = [TenantPermission]
    queryset = Products.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name","price"]
    serializer_class = ProductSerializer

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
        print(brands)            
        if params.get("o") == "popular":
            queryset = queryset.order_by("-reviews__count")
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
    queryset = Category.objects.all()

class BrandViewset(ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        payment_type = data.get("payment_type")
        save_billing_info = data.get("save_billing_info")
        region, subregion, city = data.get("region"), data.get("subregion"), data.get("city")
        
        if not hasattr(request.user, "cart"):
            raise exceptions.ValidationError({"message":"Usuario no tiene carrito de compras creado"})
        print(request.user.cart.cart_items.all())
        if not request.user.cart.cart_items.exists():
            raise exceptions.ValidationError({"message":"El carrito esta vacio"})

        total_amount = request.user.cart.total_order
        order_id = order_controller.create_order_from_cart(request.user.cart, payment_type)
        print(total_amount)

        if save_billing_info:
            # guarda la informacion y la hace principal si es que no existe
            # ninguna direccion registrada
            Address.objects.create(
                user=request.user,
                is_main=True if request.user.address.count() == 0 else False,
                region=region,
                subregion=subregion,
                city=city
            )

        if total_amount == 0:
            # Caso donde la compra es gratuita
            # TODO: link para redireccion a orden cerrada
            order_id.payment_status = OrderStatusChoices.PAYMENT_SUCCESS
            order_id.payment_method = PaymentMethodChoices.FREE_ITEM
            serializer = OrderSerializer(order_id)
            data = {**serializer.data.copy(), "href":""}
            return response.Response(serializer.data) 
        
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
        
        # caso Coinbase
        res : dict = create_charge(request.user.full_name, "descripcion de prueba", total_amount , order_id.pk)
        if not res: raise exceptions.ValidationError({
            "message":"A ocurrido un error con la pasarela de pago, no se obtuvo respuesta desde el servidor"
            })
        return response.Response(res, status=status.HTTP_202_ACCEPTED)