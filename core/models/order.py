from typing import Iterable, Optional
from django.db import models
from core.utils.model_choices import OrderStatusChoices, PaymentMethodChoices, DeliveryTypeChoices
from django.contrib.auth import get_user_model
import uuid
from django.utils.timezone import now

User = get_user_model()

class Order(models.Model):
    """
    Modelo para las ordenes relacionadas a muchos Product Order
    """
    id = models.AutoField(primary_key=True)
    payment_status = models.CharField(choices=OrderStatusChoices.CHOICES,default=OrderStatusChoices.AWAITING_PAYMENT,max_length=255,help_text="Campo para saber el status de la Transaccion")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario que creo la orden")
    external_payment_id = models.CharField(max_length=255,null=True, help_text="Las procesadoras de pago generan un id externo cuando se hace una compra, ese id debe guardarse aqui")
    payment_method = models.CharField(max_length=255, choices=PaymentMethodChoices.CHOICES, help_text="metodo elegido para el pago")
    receipt = models.FileField(null=True,upload_to="media/", help_text="Campo para hacer referencia a la ubicacion relativa del archivo del recibo de compra")
    delivery_type = models.CharField(max_length=100, choices=DeliveryTypeChoices.CHOICES, default=DeliveryTypeChoices.PERSONALLY, help_text="Campo para saber como el cliente va a retirar la mercancia")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de la Compra")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de modificacion de la compra")
    total_amount = models.FloatField(default=0, help_text="monto total de la orden de compra")

    def save(self, *args, **kwargs):
        if self.payment_status == OrderStatusChoices.PAYMENT_SUCCESS and not self.external_payment_id:
            raise ValueError("No se le puede asignar un status exitoso a una orden si no tiene un id de pasarela de pago (external_payment_id)")
        return super().save(*args,**kwargs)
    
    @property
    def is_order_paid(self):
        return self.payment_status == OrderStatusChoices.PAYMENT_SUCCESS
    @property
    def total_order(self):
        return self.product_orders.all().aggregate(
            total=models.Sum(models.F("product__price")*models.F("quantity"), output_field=models.FloatField())
             ).get("total", 0) or 0