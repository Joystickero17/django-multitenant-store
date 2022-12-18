from rest_framework import serializers
from core.models.product import Products
from core.models.wishlist import Wish
from core.serializers.product_serializer import ProductSerializer



class WishSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), source='product',write_only=True)
    in_cart = serializers.SerializerMethodField()
    class Meta:
        model = Wish
        fields= [
            "id",
            "user",
            "product",
            "product_id",
            "in_cart"
            ]
        extra_kwargs = {
            "user": {"required":False}
        }

    def get_in_cart(self, instance):
        products = self.context["request"].user.cart.cart_items.values_list("product", flat=True)
        print(instance.product.pk, products)
        return instance.product.pk in products