from rest_framework import serializers
from core.models.media import Media
from core.models.product import Products



class ProductSerializer(serializers.ModelSerializer):
    media = serializers.RelatedField(many=True, queryset=Media.objects.all())
    class Meta:
        model = Products
        fields = "__all__"
        extra_kwargs = {"tenant": {"required":False}, "media": {"required":False}}

    def create(self, validated_data):
        return super().create(validated_data)