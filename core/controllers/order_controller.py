from typing import Literal
from core.models import Order,ProductOrder
from core.utils.model_choices import PaymentMethodChoices
from core.models.cart import Cart
from django.db.models import QuerySet




def create_order_from_cart(cart: Cart, payment_method: Literal[PaymentMethodChoices.CHOICES]) -> Order:
    if payment_method not in [item[0] for item in PaymentMethodChoices.CHOICES]:
        raise ValueError(f"payment_method no tiene un valor valido, se recibio {payment_method}")
    cart_items = cart.cart_items.all()
    order = Order.objects.create(
        user=cart.user,
        payment_method=payment_method,
        )
    product_orders = [ProductOrder(**{
        "product":item.product,
        "quantity":item.quantity,
        "order": order
    }) for item in cart_items]
    ProductOrder.objects.bulk_create(product_orders)
    order.total_amount = order.total_order
    order.save()
    return order