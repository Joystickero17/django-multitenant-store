from rest_framework import serializers





class QueryParamSerializer(serializers.Serializer):
    free_products = serializers.BooleanField(required=False)
    min_price = serializers.IntegerField(required=False)
    max_price = serializers.IntegerField(required=False)