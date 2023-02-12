from rest_framework import serializers
from core.models.product_storage import ProductStorage
from core.serializers.store_serializer import StoreSerializer


class ProductStorageSerializer(serializers.ModelSerializer):
    store_details = StoreSerializer(source="store", read_only=True)
    class Meta:
        model = ProductStorage
        fields = "__all__"
        extra_kwargs = {
            "store": {
                "read_only":True
            }
        }
    def create(self, validated_data):
        data = validated_data.copy()
        data["store"] = self.context.get("request").user.store
        return super().create(data)
    
    def update(self, instance, validated_data):
        data = validated_data.copy()
        data["store"] = self.context.get("request").user.store
        return super().update(instance, data)