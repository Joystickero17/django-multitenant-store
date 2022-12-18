from django.db import models
from django.db.models.constraints import UniqueConstraint
from core.models.cart import Cart
from core.models.order import Order
from core.models.product import Products
from django.utils.timezone import now


class ProductOrder(models.Model):
    """
    Modelo para representar suborden a orden principal
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,help_text="Orden principal",related_name="product_orders")
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
        constraints = [
            UniqueConstraint("order", "product", name="unique_product_order" ,violation_error_message="No pueden haber mas de 2 ordenes de producto por orden principal"),
            ]


class CartItem(models.Model):
    """
    Modelo para representar un item del carrito
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="cart_product_items")
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
        constraints = [
            UniqueConstraint("cart", "product", name="unique_cart_product_item" ,violation_error_message="No pueden haber mas de 2 ordenes de producto por carrito"),
            ]