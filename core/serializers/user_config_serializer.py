from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models.store import Store
from core.serializers.store_serializer import StoreSerializer
from core.serializers.address_serializer import AddressSerializer

User = get_user_model()


class UserConfigSerializer(serializers.ModelSerializer):
    store_details = StoreSerializer(read_only=True, source="store")
    addresses = AddressSerializer(many=True, required=False)
    main_address = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["email",
                  "profile_img",
                  "first_name",
                  "last_name",
                  "about",
                  "is_active",
                  "is_staff",
                  "role",
                  "date_joined",
                  "main_address",
                  "born_date",
                  'addresses',
                  'phone_number',
                  "store_details",
                  "store"]
        extra_kwargs = {
            "email": {"read_only":True}
        }
    
    def get_main_address(self, obj):
        address = obj.addresses.filter(is_main=True).first()
        if not address: return
        serializer = AddressSerializer(address)
        return serializer.data
    
    def update(self, instance, validated_data):
        
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
