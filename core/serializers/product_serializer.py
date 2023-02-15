from rest_framework import serializers, exceptions
from core.models.brand import Brand
from core.models.media import Media
from core.models.product import Products
from core.models import Review
from core.serializers.abstract_serializer import AbstractEntitySerializer
from core.serializers.brand_serializer import BrandSerializer
from core.serializers.category_serializer import CategorySerializer, Category
from core.serializers.store_serializer import StoreSerializer
from core.serializers.image_serializer import UrlImageSerializer
from core.serializers.product_storage_serializer import ProductStorageSerializer


class ProductSerializer(AbstractEntitySerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True,source='category', queryset=Category.objects.all())
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(write_only=True,source='brand',allow_null=True, queryset=Brand.objects.all())
    store = StoreSerializer(read_only=True)
    photos = UrlImageSerializer(many=True, required=False)
    thumbnail = UrlImageSerializer(read_only=True)
    review_list_by_stars = serializers.SerializerMethodField()
    product_storage_details = ProductStorageSerializer(source="product_storage", read_only=True)
    
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
            "condition",
            "product_storage",
            "product_storage_details",
            "photos"
            ]
        extra_kwargs = {"store": {"read_only":True}, "photos": {"required":False}, "thumbnail":{"read_only":True}, "product_slug":{"read_only":True}}



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
        if value <=0:
            raise serializers.ValidationError("Cantidad debe ser mayor a 0")
        return value
    
    def create(self, validated_data):
        images = validated_data.pop("photos", None)
        for media in images:
            media.get("id").priority = media["priority"]
            media.get("id").save()
        instance = super().create(validated_data)
        thumbnail = next((image["id"] for image in images if image["is_thumbnail"]), None)
        if not thumbnail:
            raise exceptions.ValidationError("Debe Escoger un Thumbnail para el producto entre las imagenes proporcionadas")
        instance.thumbnail = thumbnail
        instance.save()
        media_files = [image["id"] for image in images]
        instance.photos.set(media_files)
        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop("photos", None)
        instance = super().update(instance, validated_data)
        thumbnail = next((image["id"] for image in images if image["is_thumbnail"]), None)
        if not thumbnail and not instance.thumbnail:
            raise exceptions.ValidationError("Debe Escoger un Thumbnail para el producto entre las imagenes proporcionadas")
        
        if thumbnail:
            instance.thumbnail = thumbnail
        instance.save()
        for media in images:
            media.get("id").priority = media["priority"]
            media.get("id").save()
        media_files = [image["id"] for image in images]
        instance.photos.set(media_files)
        return instance
        
class ExportProductSerializer(serializers.ModelSerializer):
    category_name=serializers.SerializerMethodField()
    brand_name=serializers.SerializerMethodField()
    store_name=serializers.SerializerMethodField()
    condition_display=serializers.SerializerMethodField()
    product_storage_address=serializers.SerializerMethodField()
    thumbnail_url =serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "category_name",
            "brand_name",
            "description",
            "product_slug",
            "rating",
            "price",
            "thumbnail_url",
            "quantity",
            "store_name",
            "condition_display",
            "product_storage_address",
            ]
    
    def get_thumbnail_url(self, obj):
        if not obj.thumbnail: return
        if not obj.thumbnail.file: return
        return obj.thumbnail.file.url

    def get_product_storage_address(self, obj):
        if not obj.product_storage: return
        return f"{obj.product_storage.region},{obj.product_storage.subregion},{obj.product_storage.city or ''}"
    
    def get_category_name(self, obj):
        if not obj.category: return
        return obj.category.name
    
    def get_brand_name(self, obj):
        if not obj.brand: return
        return obj.brand.name
    
    def get_store_name(self, obj):
        if not obj.store: return
        return obj.store.name
    
    def get_condition_display(self, obj):
        if not obj.condition: return
        return obj.get_condition_display()