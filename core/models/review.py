from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from core.models import Products



User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=1000)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    class Meta:
        ordering = ["-created_at"]