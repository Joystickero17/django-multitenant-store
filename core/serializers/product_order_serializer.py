from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from core.models.product import Products

from core.models.product_order import ProductOrder



class TinyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

class ProductOrderSerializer(serializers.ModelSerializer):
    product_details = TinyProductSerializer(read_only=True, source="product")
    class Meta:
        model = ProductOrder
        fields = "__all__"
        extra_kwargs = {
            "product":{
                "write_only": True
            }
        }
        # validators = [
        #         UniqueTogetherValidator(
        #             queryset=ProductOrder.objects.all(),
        #             fields=['cart', 'product'],
        #             message="Ya existe este producto en tu carrito"
        #         )
        #     ]