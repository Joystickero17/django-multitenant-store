from rest_framework import serializers
from core.models.order import Order




class ManualMarkOrderSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    is_paid = serializers.BooleanField()