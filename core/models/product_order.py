from django.db import models
from django.db.models.constraints import UniqueConstraint
from core.models.cart import Cart
from core.models.product import Products
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from core.models.purchase import Purchase
User = get_user_model()


class ProductOrder(models.Model):
    """
    Modelo para pedido de producto
    """
    cart = models.ForeignKey(Cart, null=True,on_delete=models.CASCADE, related_name="product_orders")
    purchase = models.ForeignKey(Purchase, null=True,on_delete=models.CASCADE, related_name="product_orders")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_orders")
    quantity = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    def save(self, *args,**kwargs):
        if not self.product.quantity:
            raise ValueError(f"el producto {self.product.name} no tiene existencias")
        if self.product.quantity < self.quantity:
            raise ValueError(f"el producto {self.product.name} solo tiene {self.product.quantity}, se esta asignando {self.quantity} en esta orden")
        return super().save(*args, **kwargs)
    class Meta:
        ordering = ["-created_at"]
        constraints = [UniqueConstraint("cart", "product", name="unique_cart_product_order" ,violation_error_message="No pueden haber mas de 2 ordenes de producto por carrito")]