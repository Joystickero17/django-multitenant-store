from rest_framework import serializers

from core.models.product_order import ProductOrder


class AmountItemSerializer(serializers.Serializer):
    currency_code = serializers.CharField()
    value = serializers.FloatField()
    reference_id = serializers.UUIDField()

    def to_representation(self, instance):
        data = super().to_representation(instance).copy()
        data["value"] = str(data["value"])
        data["reference_id"] = str(data["reference_id"])
        return data


class PaypalItemsSerializer(serializers.Serializer):
    amount = AmountItemSerializer()