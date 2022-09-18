from rest_framework import serializers
from core.models import Store
from drf_extra_fields.fields import Base64ImageField

class StoreSerializer(serializers.ModelSerializer):
    logo = Base64ImageField()
    class Meta:
        model = Store
        fields = "__all__"
        extra_kwargs = {
            'child':{"required":False}
        }

