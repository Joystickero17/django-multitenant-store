from rest_framework import serializers, exceptions
from core.choices.model_choices import RoleChoices
from core.models.order import Order
from core.models.product_order import ProductOrder
from core.serializers.product_order_serializer import ProductOrderSerializer
from core.serializers.user_serializer import CoreUserSerializer
from core.serializers.external_payment_serializer import ExternalPaymentSerializer
from django.contrib.auth import get_user_model
from core.serializers.address_serializer import AddressSerializer
from core.utils.model_choices import OrderStatusChoices

User = get_user_model()
class PrivateUserSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "profile_img",
            "store",
            "store_name",
            "first_name",
            "last_name",
            "total_orders"
        ]
    
    def get_store_name(self, obj):
        if not obj.store: return
        return obj.store.name
    
    def get_total_orders(self, instance):
        orders = instance.order_set.all()
        request =  self.context.get("request")
        if not request: return orders.count()
        if request.user.role == RoleChoices.WEBSITE_OWNER: return orders.count()
        user = request.user
        if not user: return orders.count()
        return orders.filter(product_orders__product__store=user.store).distinct().count()

class ExportContactSerializer(PrivateUserSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "store_name",
            "first_name",
            "last_name",
            "total_orders"
        ]

class StoreOrderSerializer(serializers.ModelSerializer):
    product_orders = ProductOrderSerializer(many=True)
    delivery_type_verbose = serializers.CharField(source="get_delivery_type_display")
    payment_type_verbose = serializers.CharField(source="get_payment_method_display")
    total_order = serializers.FloatField()
    user_details = PrivateUserSerializer(source="user")
    external_payments = ExternalPaymentSerializer(many=True)
    address_details = AddressSerializer(source="address")
    class Meta:
        model = Order
        fields = "__all__"
    
    # def to_internal_value(self, data):
    #     new_data = data.copy()
    #     new_data["user"] = self.context["request"].user
    #     return super().to_internal_value(data)

    # def validate(self, attrs):
    #     user = self.context["request"].user
    #     if not user.cart.cart_items.exists():
    #         raise exceptions.ValidationError({"message": "el carrito esta vacio, no se puede crear la orden"})

    #     if user.orders.count() == 1 and not self.request.orders.first().paid:
    #         raise exceptions.ValidationError({"message":"no se puede tener mas de una orden no pagada, si crees que se trata de un error comunicate con soporte."})
        
    #     for item in user.cart.cart_items.all():
    #         if item.product.quantity < item.quantity:
    #             raise exceptions.ValidationError({"message":f"el producto con id {item.product.pk}, {item.product.name} solo posee {item.product.quantity} y se esta ordenando {item.quantity}"})

    #     return super().validate(attrs)

    # def create(self, validated_data):
    #     order = super().create(validated_data)
    #     product_orders = [ProductOrder(product=order.product,quantity=order.quantity,) for order in self.request.cart.cart_items]
    #     if not product_orders:
    #         raise exceptions.ValidationError({"message":"No existen productos en el carrito"})
    #     ProductOrder.objects.bulk_create(product_orders)
    #     order.product_orders.set(product_orders)
    #     return order


class ExportOrderSerializer(serializers.ModelSerializer):
    receipt_url = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    payment_status_display = serializers.SerializerMethodField()
    delivery_type_display = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'id',
            'payment_method',
            'receipt_url',
            'delivery_type_display',
            'created_at',
            'user_email',
            'payment_status_display',
            'total_amount'
        ]

    def get_delivery_type_display(self, obj):
        if not obj.delivery_type: return
        return obj.get_delivery_type_display()
    
    def get_payment_status_display(self, obj):
        if not obj.payment_status: return
        return obj.get_payment_status_display()
    
    def get_user_email(self, obj):
        if not obj.user: return
        return obj.user.email

    def get_receipt_url(self, obj):
        if not obj.receipt: return
        return obj.receipt.url


class OrderSerializer(serializers.ModelSerializer):
    product_orders = ProductOrderSerializer(many=True)
    delivery_type_verbose = serializers.CharField(source="get_delivery_type_display")
    class Meta:
        model = Order
        extra_kwargs = {
            "paid": {
                "read_only": True
            }
        }
        exclude = ["user"]
        # fields = "__all__"
    
    def to_internal_value(self, data):
        new_data = data.copy()
        new_data["user"] = self.context["request"].user
        return super().to_internal_value(data)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.cart.cart_items.exists():
            raise exceptions.ValidationError({"message": "el carrito esta vacio, no se puede crear la orden"})

        if user.orders.count() == 1 and not self.request.orders.first().paid:
            raise exceptions.ValidationError({"message":"no se puede tener mas de una orden no pagada, si crees que se trata de un error comunicate con soporte."})
        
        for item in user.cart.cart_items.all():
            if item.product.quantity < item.quantity:
                raise exceptions.ValidationError({"message":f"el producto con id {item.product.pk}, {item.product.name} solo posee {item.product.quantity} y se esta ordenando {item.quantity}"})

        return super().validate(attrs)

    def create(self, validated_data):
        order = super().create(validated_data)
        product_orders = [ProductOrder(product=order.product,quantity=order.quantity,) for order in self.request.cart.cart_items]
        if not product_orders:
            raise exceptions.ValidationError({"message":"No existen productos en el carrito"})
        ProductOrder.objects.bulk_create(product_orders)
        order.product_orders.set(product_orders)
        return order