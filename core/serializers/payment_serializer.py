from rest_framework import serializers
from core.utils.model_choices import DeliveryTypeChoices, PaymentMethodChoices
from core.models.user_data.address import Address

class PaymentSerializer(serializers.Serializer):
    save_billing_info = serializers.BooleanField(default=True)
    name = serializers.CharField()
    last_name = serializers.CharField()
    short_address = serializers.CharField()
    user_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)
    region = serializers.CharField()
    subregion = serializers.CharField()
    city = serializers.CharField()
    zip_code: serializers.CharField()
    phone_number = serializers.CharField()
    payment_type = serializers.ChoiceField(choices=PaymentMethodChoices.CHOICES)
    aditional_info = serializers.CharField(required=False, allow_null=True)
    delivery_type = serializers.ChoiceField(choices=DeliveryTypeChoices.CHOICES)
    message = serializers.CharField(required=False, allow_blank=True)
