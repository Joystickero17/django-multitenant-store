from rest_framework import serializers, exceptions
from core.models.product_order import CartItem
from core.serializers.product_serializer import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(read_only=True, source="product")
    class Meta:
        model = CartItem
        fields = "__all__"