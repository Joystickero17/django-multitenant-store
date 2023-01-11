from rest_framework import serializers
from core.models.media import Media
from drf_extra_fields.fields import Base64ImageField




class ImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField()
    class Meta:
        model = Media
        fields = "__all__"