from django.contrib.auth import get_user_model
from core.models.product import Products
from django.db import models


User = get_user_model()

class Wish(models.Model):
    """
    elemento de la lista de deseos
    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="wish_list", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.user.email}"
    
    class Meta:
        constraints= [
            models.UniqueConstraint(fields=["product","user"], name="unique product per user")
        ]