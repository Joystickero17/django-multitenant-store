from typing import Literal
from core.models import Order,ProductOrder
from core.tasks import send_receipt
from core.utils.model_choices import PaymentMethodChoices,OrderStatusChoices
from core.models.user_data.address import Address
from core.models.cart import Cart
from django.db.models import QuerySet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()





def create_order_from_cart(cart: Cart, payment_method: Literal[PaymentMethodChoices.CHOICES], **kwargs) -> Order:
    if payment_method not in [item[0] for item in PaymentMethodChoices.CHOICES]:
        raise ValueError(f"payment_method no tiene un valor valido, se recibio {payment_method}")
    cart_items = cart.cart_items.all()
    address = kwargs.get("address")
    if address:
        if not isinstance(address,Address):
            raise ValueError(f"{address} no es de tipo {Address}")

    order = Order.objects.create(
        user=cart.user,
        payment_method=payment_method,
        address=address
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
    # Task Asincrona para enviar el correo del recibo
    send_receipt.delay(order.id)

    for item in order.product_orders.all():
        async_to_sync(channel_layer.group_send)(f"store_{item.product.store.slug}",{"type":"chat.message","message":"Ha habido una nueva compra"})
    return order

def on_payment_reject(order: Order) -> Order:
    # TODO: enviar correo de pago fallido
    order.payment_status = OrderStatusChoices.PAYMENT_FAILED
    order.save()
    return order