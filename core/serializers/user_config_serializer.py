from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models.store import Store
from core.serializers.store_serializer import StoreSerializer
from core.serializers.address_serializer import AddressSerializer
from drf_extra_fields.fields import Base64ImageField
from core.models.user_data.payment_methods import PaymentMethod
User = get_user_model()

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "type",
            "account_number",
            "email_adress",
            "phone_number",
            "national_bank",
        ]

class UserConfigSerializer(serializers.ModelSerializer):
    store_details = StoreSerializer(read_only=True, source="store")
    profile_img = Base64ImageField()
    addresses = AddressSerializer(many=True, required=False)
    main_address = serializers.SerializerMethodField()
    payment_methods = PaymentMethodSerializer(many=True,required=False)

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
            "payment_methods",
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
        payment_methods = validated_data.pop("payment_methods",None)
        instance = super().update(instance,validated_data)
        if payment_methods:
            pm = [PaymentMethod.objects.create(**method) for method in payment_methods]
            instance.payment_methods.set(pm)
        else:
            instance.payment_methods.set([])

        if profile_img:
            instance.profile_img.save(profile_img.name, profile_img)
        return instance
