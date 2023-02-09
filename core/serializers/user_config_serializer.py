from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models.store import Store
from core.serializers.store_serializer import StoreSerializer
from core.serializers.address_serializer import AddressSerializer
from drf_extra_fields.fields import Base64ImageField
User = get_user_model()


class UserConfigSerializer(serializers.ModelSerializer):
    store_details = StoreSerializer(read_only=True, source="store")
    profile_img = Base64ImageField()
    addresses = AddressSerializer(many=True, required=False)
    main_address = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
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
            "store",
            "credits"
        ]
        extra_kwargs = {
            "email": {"read_only": True}
        }

    def get_main_address(self, obj):
        address = obj.addresses.filter(is_main=True).first()
        if not address:
            return
        serializer = AddressSerializer(address)
        return serializer.data
    
    def update(self, instance, validated_data):
        profile_img = validated_data.pop("profile_img", None)
        instance = super().update(instance,validated_data)
        if profile_img:
            instance.profile_img.save(profile_img.name, profile_img)
        return instance
