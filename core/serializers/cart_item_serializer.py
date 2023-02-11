from rest_framework import serializers, exceptions
from core.models.product_order import CartItem
from core.serializers.product_serializer import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(read_only=True, source="product")
    def validate(self, attrs):
        data = super().validate(attrs)
        product = data["product"]
        if product.quantity == 0:
            raise exceptions.ValidationError("El producto no tiene existencias, por favor intente más tarde")
        return data
    class Meta:
        model = CartItem
        fields = "__all__"