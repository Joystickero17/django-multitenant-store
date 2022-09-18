from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email",
                  "first_name",
                  "last_name",
                  "about",
                  "is_active",
                  "is_staff",
                  "role",
                  "date_joined",
                  "born_date",
                  "store"]
        extra_kwargs = {
            "email": {"read_only":True}
        }
    
    def update(self, instance, validated_data):
        
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
