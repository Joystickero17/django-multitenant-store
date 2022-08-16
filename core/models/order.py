from .product import Products, models


class Order(models.Model):
    sub_total = models.FloatField()
    total = models.FloatField()


class SubOrder(models.Model):
    checkout = models.ForeignKey(Order, related_name="parent_order", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
