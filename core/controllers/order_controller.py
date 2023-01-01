from typing import Literal
from core.models import Order,ProductOrder
from core.utils.model_choices import PaymentMethodChoices,OrderStatusChoices
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
    #cart.cart_items.all().delete()
    return order

def on_payment_aprove(order: Order)-> Order:
    """
    Ejecutar aqui todo lo que deba pasar cuando se paga una orden
    """
    # TODO: enviar recibo
    # TODO: sumar creditos a empresas de los productos
    order.payment_status = OrderStatusChoices.PAYMENT_SUCCESS
    order.save()
    return order

def on_payment_reject(order: Order) -> Order:
    # TODO: enviar correo de pago fallido
    order.payment_status = OrderStatusChoices.PAYMENT_FAILED
    order.save()
    return order