from rest_framework import serializers
from core.models.order import Order




class PagoMovilSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    reference = serializers.CharField()