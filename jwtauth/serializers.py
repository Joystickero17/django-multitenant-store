from rest_framework import serializers
from django.contrib.auth import get_user_model, hashers
from rest_framework.exceptions import ValidationError

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password_confirm = serializers.CharField()
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm"
            ]

    def validate(self, attrs):
        confirmed_password = attrs.pop("password_confirm")
        if attrs.get("password") != confirmed_password:
            raise ValidationError("las contraseñas no coinciden")
        return attrs
    
    def to_representation(self, instance):
        user = {"email":instance.email, "is_active":instance.is_active}
        return user
        
    def create(self, validated_data):
        password = hashers.make_password(validated_data.get("password"))
        created_user = User.objects.create(email=validated_data.get("email"), password=password)
        
        return created_user