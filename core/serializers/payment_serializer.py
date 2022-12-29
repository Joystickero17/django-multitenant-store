from rest_framework import serializers
from core.utils.model_choices import DeliveryTypeChoices, PaymentMethodChoices


class PaymentSerializer(serializers.Serializer):
    save_billing_info = serializers.BooleanField()
    name = serializers.CharField()
    last_name = serializers.CharField()
    short_address = serializers.CharField()
    region = serializers.CharField()
    subregion = serializers.CharField()
    city = serializers.CharField()
    zip_code: serializers.CharField()
    phone_number = serializers.CharField()
    payment_type = serializers.ChoiceField(choices=PaymentMethodChoices.CHOICES)
    delivery_type = serializers.ChoiceField(choices=DeliveryTypeChoices.CHOICES)
    message = serializers.CharField(required=False, allow_blank=True)