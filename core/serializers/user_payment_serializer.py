from rest_framework import serializers, exceptions
from core.models.user_payment import UserPayment
from core.choices.model_choices import RoleChoices
from django.utils.timezone import now

class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = UserPayment
        extra_kwargs = {
            "user":{
                "read_only":True
            },
            'payment_date':{
                'read_only':True
            }
        }
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.context.get("request").user
        is_freelance = user.role == RoleChoices.FREELANCE
        is_store_owner = user.role == RoleChoices.STORE_OWNER
        
        if user.role not in [RoleChoices.FREELANCE,RoleChoices.STORE_OWNER]:
            raise exceptions.ValidationError({"message":"No está autorizado para realizar esta acción"})
        if attrs["money"] <= 0:
            raise exceptions.ValidationError({"message":"la cantidad a retirar debe ser mayor a cero"})
        if is_freelance:
            if attrs["money"] > user.credits/1000:
                raise exceptions.ValidationError({"message":"Créditos Insuficientes"})
        elif is_store_owner:
            if attrs["money"] > user.store.money:
                raise exceptions.ValidationError({"message":"Créditos Insuficientes"})
        
        return data
    
    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["paid"] = False
        validated_data['user'] = user
        is_freelance = user.role == RoleChoices.FREELANCE
        is_store_owner = user.role == RoleChoices.STORE_OWNER
        if not (is_freelance or is_store_owner):
            raise exceptions.ValidationError({"message":"Rol no autorizado para hacer retiros, solo los StoreOwner pueden realizarlo"})
        if is_freelance:
            user.credits -= validated_data["money"]*1000
            user.save()
        elif is_store_owner:
            user.store.money -= validated_data["money"]
            user.store.save()

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        user = self.context.get("request").user
        
        if user.role != RoleChoices.WEBSITE_OWNER:
            raise exceptions.ValidationError({"message":"Solo los Store Owners pueden cambiar el estado de un pago"})

        if validated_data.get("paid"):
            instance.payment_date = now()
            instance.save()
        return super().update(instance, validated_data)