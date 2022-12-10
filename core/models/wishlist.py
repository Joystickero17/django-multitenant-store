from django.contrib.auth import get_user_model
from core.models.product import Products
from django.db import models


User = get_user_model()

class Wish(models.Model):
    """
    Modelo que representa un elemento de la lista de deseos
    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE, help_text="Producto agregado a la lista de deseos")
    user = models.ForeignKey(User, related_name="wish_list",help_text="Usuario que agrego este producto a su lista", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.user.email}"
    
    class Meta:
        constraints= [
            models.UniqueConstraint(fields=["product","user"], name="unique product per user")
        ]