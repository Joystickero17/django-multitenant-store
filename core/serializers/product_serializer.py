from rest_framework import serializers
from core.models.brand import Brand
from core.models.media import Media
from core.models.product import Products
from core.serializers.abstract_serializer import AbstractEntitySerializer
from core.serializers.brand_serializer import BrandSerializer
from core.serializers.category_serializer import CategorySerializer, Category

class ProductSerializer(AbstractEntitySerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True,source='category', queryset=Category.objects.all())
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(write_only=True,source='brand',allow_null=True, queryset=Brand.objects.all())
    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "price",
            "thumbnail",
            "quantity",
            "get_discount",
            "has_stock",
            "store",
            "verbose_condition",
            ]
        extra_kwargs = {"store": {"read_only":True}, "photos": {"required":False}, "thumbnail":{"required":False}}
    
    def validate_quantity(self, value):
        if not value:
            raise serializers.ValidationError("Cantidad debe ser mayor a 0")
        return value