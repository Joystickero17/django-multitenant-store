import random
from rest_framework import serializers, exceptions
from core.choices.model_choices import RoleChoices
from core.models.assistance import Assistance
from core.models.product_order import CartItem,ProductOrder
from django.contrib.auth import get_user_model
from core.serializers.user_config_serializer import UserConfigSerializer

User = get_user_model()

class AssistanceSerializer(serializers.ModelSerializer):
    cart_items = serializers.PrimaryKeyRelatedField(queryset=CartItem.objects.all(), many=True)
    product_orders = serializers.PrimaryKeyRelatedField(queryset=ProductOrder.objects.all(), many=True, required=False)
    customer_details = UserConfigSerializer(source='customer', read_only=True)
    freelance_details = UserConfigSerializer(source='freelance', read_only=True)
    class Meta:
        model = Assistance
        fields = "__all__"
        extra_kwargs = {
            "freelance":{
                "required":False
            },
            "customer":{
                "required":False
            },
            "product_orders":{
                "required":False
            }
        }

    def create(self, validated_data):
        items = validated_data.pop("cart_items", None)
        
        product_orders = validated_data.pop("product_orders", None)
        freelancers = User.objects.filter(role=RoleChoices.FREELANCE)
        if not freelancers.exists():
            raise exceptions.ValidationError({'message':"No hay freelancers Disponibles"})
        user = random.choice(freelancers)
        data = validated_data.copy()
        data["freelance"] = user
        data["customer"] = self.context.get("request").user
        if not items:
            raise exceptions.ValidationError({
                'message':"Debe enviar los cart items que se va a asistir"
                })
        instance = super().create(data)
        instance.cart_items.set(items)
        return instance
    
    def update(self, instance, validated_data):
        items = validated_data.pop("cart_items", None)
        user = validated_data.get("freelance")
        return super().update(instance, validated_data)