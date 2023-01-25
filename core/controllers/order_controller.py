from typing import List, Literal
from core.controllers.notification_controller import create_notification
from core.models import Order,ProductOrder
from core.tasks import send_receipt
from core.utils.model_choices import PaymentMethodChoices,OrderStatusChoices
from core.models.user_data.address import Address
from core.models.cart import Cart
from django.db.models import QuerySet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth import get_user_model
from core.choices.model_choices import RoleChoices
channel_layer = get_channel_layer()
User = get_user_model()

def get_super_user_store() -> User:
    user = User.objects.filter(role=RoleChoices.WEBSITE_OWNER).first()

    if not user:
        raise ValueError(f"No esta asignado el Rol {RoleChoices.WEBSITE_OWNER}")

    if not user.store:
        raise ValueError("El Website owner no tiene una tienda creada")
    return user

def credit_store(order:Order):
    """
    Funcion que se encarga de acreditar a una empresa la ganancia correspondiente
    """
    for item in order.product_orders.all():
        # porcentaje de la tienda
        main_user = get_super_user_store()
        main_store_fee = item.sub_total * settings.MAIN_STORE_FEE
        main_user.store.money += main_store_fee
        main_user.store.save()

        # asignacion de creditos a las empresas
        item.product.store.money += item.sub_total - main_store_fee


        item.product.store.save()

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
    # TODO: sumar creditos a empresas de los productos
    order.payment_status = OrderStatusChoices.PAYMENT_SUCCESS
    order.save()
    
    # Task Asincrona para enviar el correo del recibo
    send_receipt.delay(order.id)

    # se acreditan a las tiendas y tienda principal
    credit_store(order)

    # limpieza del carrito
    order.user.cart.cart_items.all().delete()

    # descuento del inventario
    for item in order.product_orders.all():
        item.product.quantity -= item.quantity
        item.product.save()
    
    # tiendas a notificar del pago de la orden
    stores: List[str] = order.product_orders.all().values_list("product__store__slug", flat=True)
    for item in stores:
        create_notification(
            content="Ha Habido una nueva Compra", 
            entity_name="order", 
            entity_id=f"{order.id}", 
            group=f"store_{item}"
        )
    return order

def on_payment_reject(order: Order) -> Order:
    # TODO: enviar correo de pago fallido
    order.payment_status = OrderStatusChoices.PAYMENT_FAILED
    order.save()
    return order