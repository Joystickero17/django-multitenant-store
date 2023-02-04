from django.db import models
# from core.models.product_order import CartItem,ProductOrder
from django.contrib.auth import get_user_model

User = get_user_model()

class Assistance(models.Model):
    # cart_items = models.ManyToManyField(CartItem)
    # product_orders = models.ManyToManyField(ProductOrder)
    customer = models.ForeignKey(User, related_name="customer_assistances", null=True, on_delete=models.CASCADE)
    feedback = models.BooleanField(null=True)
    freelance = models.ForeignKey(User, related_name="assistances",  on_delete=models.CASCADE)
    completed = models.BooleanField(default=False, help_text="Para indicar si el freelance completo la asistencia")
