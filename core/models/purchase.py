from django.db import models
from django.utils.timezone import now


class Purchase(models.Model):
    """
    Modelo que representa una compra
    """
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de la Compra")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de modificacion de la compra")
    receipt = models.FileField(null=True,upload_to="media/", help_text="Campo para hacer referencia a la ubicacion relativa del archivo del recibo de compra")