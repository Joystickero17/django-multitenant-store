from django.db import models
from django.utils.timezone import now

class EntityChoices:
    ORDER = "order"
    PRODUCT_ORDER = "product_order"
    MESSAGE = "message"
    CHOICES = [
        (ORDER, "Orden"),
        (MESSAGE, "Mensaje"),
        (PRODUCT_ORDER, "Orden de Producto")
    ]

class ChannelGroup(models.Model):
    """
    Group para comunicacion de Channels
    """
    name = models.CharField(unique=True, max_length=500)


class Notification(models.Model):
    """
    Modelo para una notificacion push por channels
    """
    entity_name = models.CharField(max_length=255, choices=EntityChoices.CHOICES)
    message = models.TextField(max_length=1500)
    entity_id = models.PositiveBigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)
    channel_group = models.ForeignKey(ChannelGroup, null=True, on_delete=models.CASCADE)