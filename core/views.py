from itertools import product
from operator import xor
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import views
from rest_framework import permissions, exceptions
from rest_framework import pagination
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework import response
from django.db.models.query_utils import Q
from django.db.models import Max, Sum
from core.models import Store, Products
from core.models.cart import Cart
from core.models.order import Order
from core.models.product_order import CartItem, ProductOrder
from core.models.wishlist import Wish
from core.permissions.wish_permission import SameUserPermission
from core.serializers.brand_serializer import BrandSerializer, Brand
from core.serializers.cart_item_serializer import CartItemSerializer
from core.serializers.category_serializer import CategorySerializer, Category
from core.serializers.order_serializer import OrderSerializer
from core.serializers.product_order_serializer import ProductOrderSerializer
from core.serializers.product_serializer import ProductSerializer
from core.serializers.query_param_serializer import QueryParamSerializer
from core.serializers.store_serializer import StoreSerializer
from core.serializers.user_config_serializer import UserConfigSerializer
from core.serializers.review_serializer import ReviewSerializer, Review
from core.serializers.wish_serializer import WishSerializer
from .permissions.tenant_permission import TenantPermission
from django.contrib.auth import get_user_model

User = get_user_model()


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


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()