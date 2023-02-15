from rest_framework import serializers, exceptions
from core.models.product_order import ProductOrder
from core.utils.model_choices import OrderStatusChoices, ChartTypeChoices
from core.models.store import Store
from django.db.models import QuerySet


class HistoricSalesSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField(required=False)
    chart_type = serializers.ChoiceField(choices=ChartTypeChoices.CHOICES, default=ChartTypeChoices.YEAR)
    store_stats_only = serializers.BooleanField(default=True)

    
    def validate(self, attrs):
        data = super().validate(attrs)
        if data["chart_type"] == ChartTypeChoices.YEAR:
            return data
        if data["chart_type"] == ChartTypeChoices.MONTH and not data.get('month'):
            raise exceptions.ValidationError("El mes es requerido")
        if not(1 <= data.get("month") <= 12):
            raise exceptions.ValidationError("El mes proporcionado es invalido")
        return data
