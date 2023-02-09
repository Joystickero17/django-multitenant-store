from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User =get_user_model()

class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    money = models.FloatField()
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)
