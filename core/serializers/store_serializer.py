from rest_framework import serializers, exceptions
from core.models import Store
from django.utils.text import slugify
from drf_extra_fields.fields import Base64ImageField


class StoreSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(required=False)
    slug = serializers.CharField(read_only=True)
    class Meta:
        model = Store
        fields = "__all__"
        extra_kwargs = {
            'child':{"required":False}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs) 
        slug = slugify(attrs["name"])
        store = Store.objects.filter(slug=slug).first()
        if store:
            raise exceptions.ValidationError(f"La tienda '{store.name}' ya existe por favor regresa y escoge otro nombre, si crees que se trata de un error por favor contacta al soporte")
        return attrs