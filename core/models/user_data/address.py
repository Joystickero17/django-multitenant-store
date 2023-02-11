from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class Address(models.Model):
    """
    Modelo utilizado para representar o bien una direccion de principal, de facturacion, o de envio
    """
    google_coordinates = models.CharField(max_length=255, help_text="Coordenadas de Google Maps", null=True)
    is_main = models.BooleanField(default=True, help_text="Indica si la direccion es principal o no")
    name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario que registro esta direccion", related_name="addresses")
    region = models.CharField(max_length=255, help_text="Estado o Region de la direccion", null=True)
    subregion = models.CharField(max_length=255, help_text="ciudad de la direccion", null=True)
    city = models.CharField(max_length=255, help_text="Localidad, calle o Avenida de la direccion", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=now, help_text="campo para saber la creacion")
    updated_at = models.DateTimeField(auto_now=now, help_text="campo para saber cuando se actualizo la direccion")
    short_address = models.CharField(max_length=500, help_text="Detalles de la direccion actual para fines de posicionamiento a la hora de envio", null=True)
    contact_phone = models.CharField(max_length=255, help_text="Telefono Alternativo de Contacto")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user",],condition=models.Q(is_main=True), name="unique_main_address_user")
        ]