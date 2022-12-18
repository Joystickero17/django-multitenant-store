from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ShippingInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario al que perteneces esta informacion de envio")
    