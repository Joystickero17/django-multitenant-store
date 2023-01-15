from rest_framework import serializers
from core.models.media import Media
from drf_extra_fields.fields import Base64ImageField




class UrlImageSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Media.objects.all())
    file = serializers.URLField()
    name = serializers.CharField()
    is_thumbnail = serializers.BooleanField(default=False, write_only=True)
    priority = serializers.IntegerField(default=0)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["file"] = instance.file.url
        return data

class ImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField()
    class Meta:
        model = Media
        fields = "__all__"