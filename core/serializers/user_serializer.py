from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email", "profile_img"]