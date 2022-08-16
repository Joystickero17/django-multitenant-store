from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions
from core.models import Store, Products
from core.serializers.product_serializer import ProductSerializer
from core.serializers.store_serializer import StoreSerializer
from core.serializers.user_config_serializer import UserConfigSerializer
from .permissions.tenant_permission import TenantPermission
from django.contrib.auth import get_user_model

User = get_user_model()
class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StoreSerializer

class ProductViewSet(ModelViewSet):
    permission_classes = [TenantPermission]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class UserConfigView(ModelViewSet):
    serializer_class = UserConfigSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
