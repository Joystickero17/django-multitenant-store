from rest_framework import serializers
from core.models.product import Products
from core.models.wishlist import Wish
from core.serializers.product_serializer import ProductSerializer



class WishSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), source='product',write_only=True)
    class Meta:
        model = Wish
        fields= [
            "id",
            "user",
            "product",
            "product_id"
            ]
        extra_kwargs = {
            "user": {"required":False}
        }