from rest_framework import serializers
from core.models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"
        extra_kwargs = {
            'child':{"required":False}
        }