from rest_framework import serializers
from core.models import Brand





class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = [
            "created_at",
            "updated_at"
                    ]