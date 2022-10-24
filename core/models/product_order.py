from django.db import models
from core.models.product import Products
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()


class ProductOrder(models.Model):
    """
    Modelo que actuara como carrito cuando se agrupe por usuario
    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_orders")
    quantity = models.PositiveBigIntegerField()
    costumer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        ordering = ["-created_at"]