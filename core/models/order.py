from django.db import models
from core.utils.model_choices import PaymentMethodChoices
from django.contrib.auth import get_user_model
import uuid
from django.utils.timezone import now

User = get_user_model()

class Order(models.Model):
    """
    Modelo para las ordenes relacionadas a muchos Product Order
    """
    id = models.UUIDField(default=uuid.uuid4, help_text="Campo de identificacion unico", primary_key=True)
    paid = models.BooleanField(default=False, help_text="Campo para saber si la orden fue pagada")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario que creo la orden")
    external_payment_id = models.CharField(max_length=255,null=True, help_text="Las procesadoras de pago generan un id externo cuando se hace una compra, ese id debe guardarse aqui")
    payment_method = models.CharField(max_length=255, choices=PaymentMethodChoices.CHOICES, help_text="metodo elegido para el pago")
    receipt = models.FileField(null=True,upload_to="media/", help_text="Campo para hacer referencia a la ubicacion relativa del archivo del recibo de compra")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de la Compra")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de modificacion de la compra")

