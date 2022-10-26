from rest_framework import serializers
from core.models import Review
from core.serializers.user_serializer import UserSerializer



class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Review
        fields = "__all__"

    
        