from django.db import models
from django.contrib.auth import get_user_model
from core.utils.model_choices import OrderStatusChoices
import uuid

User = get_user_model()
class Cart(models.Model):
    """
    Modelo para representar un carrito de compras del usuario
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart", help_text="Usuario a quien pertenece el carrito")
    sub_total = models.FloatField(default=0, help_text="Subtotal de los productos del carrito")
    total = models.FloatField(default=0, help_text="Total del producto del carrito")
