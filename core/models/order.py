from django.db import models
from core.models.product_order import ProductOrder
from django.contrib.auth import get_user_model
from core.utils.model_choices import OrderStatusChoices

User = get_user_model()
class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, null=True)
    product_orders = models.ManyToManyField(ProductOrder)
    state = models.CharField(max_length=100,choices=OrderStatusChoices.CHOICES, default=OrderStatusChoices.IN_CART)
    sub_total = models.FloatField(default=0)
    total = models.FloatField(default=0)
