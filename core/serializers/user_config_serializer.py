from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models.store import Store
from core.serializers.store_serializer import StoreSerializer

User = get_user_model()


class UserConfigSerializer(serializers.ModelSerializer):
    store_details = StoreSerializer(read_only=True, source="store")
    class Meta:
        model = User
        fields = ["email",
                  "first_name",
                  "last_name",
                  "about",
                  "is_active",
                  "is_staff",
                  "role",
                  "date_joined",
                  "born_date",
                  "store_details",
                  "store"]
        extra_kwargs = {
            "email": {"read_only":True}
        }
    
    def update(self, instance, validated_data):
        
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
