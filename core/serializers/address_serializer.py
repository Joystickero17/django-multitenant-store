from rest_framework import serializers, exceptions
from core.models.user_data.address import Address




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"