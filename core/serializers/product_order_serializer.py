from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models.product_order import ProductOrder





class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = "__all__"
        # validators = [
        #         UniqueTogetherValidator(
        #             queryset=ProductOrder.objects.all(),
        #             fields=['cart', 'product'],
        #             message="Ya existe este producto en tu carrito"
        #         )
        #     ]