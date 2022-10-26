from rest_framework import serializers
from core.models.brand import Brand
from core.models.media import Media
from core.models.product import Products
from core.models import Review
from core.serializers.abstract_serializer import AbstractEntitySerializer
from core.serializers.brand_serializer import BrandSerializer
from core.serializers.category_serializer import CategorySerializer, Category
from core.serializers.store_serializer import StoreSerializer

class ProductSerializer(AbstractEntitySerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True,source='category', queryset=Category.objects.all())
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(write_only=True,source='brand',allow_null=True, queryset=Brand.objects.all())
    store = StoreSerializer(read_only=True)
    review_list_by_stars = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "description",
            "product_slug",
            "rating",
            "price",
            "thumbnail",
            "quantity",
            "get_discount",
            "review_list_by_stars",
            "has_stock",
            "store",
            "verbose_condition",
            ]
        extra_kwargs = {"store": {"read_only":True}, "photos": {"required":False}, "thumbnail":{"required":False}}

    def get_review_list_by_stars(self, obj):
        return {
            "five":Review.objects.filter(product=obj, score=5).count(),
            "four":Review.objects.filter(product=obj, score=4).count(),
            "three":Review.objects.filter(product=obj, score=3).count(),
            "two":Review.objects.filter(product=obj, score=2).count(),
            "one":Review.objects.filter(product=obj, score=1).count()
        }

    def validate_quantity(self, value):
        if not value:
            raise serializers.ValidationError("Cantidad debe ser mayor a 0")
        return value