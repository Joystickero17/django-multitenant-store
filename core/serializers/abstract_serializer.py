from django.forms import ValidationError
from rest_framework import serializers


class AbstractSerializer(serializers.Serializer):
    tenant_id = serializers.CharField(read_only=True)

    # def validate_tenant_id(self, value):
    #     current_user = self.context.get("request").user
    #     if not current_user.tenant_id:
    #         raise ValidationError("El usuario no tiene ningun tenant id asignado, por favor contactar a soporte")
    #     try:

    #     return True