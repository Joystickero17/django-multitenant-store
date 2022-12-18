from rest_framework import serializers, exceptions
from core.models.order import Order
from core.models.product_order import ProductOrder

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {
            "paid": {
                "read_only": True
            }
        }
        exclude = ["user"]
    
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