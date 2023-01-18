from rest_framework import serializers
from core.models.external_payments import ExternalPayment



class ExternalPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalPayment
        fields = "__all__"



