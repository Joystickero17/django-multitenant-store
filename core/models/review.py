from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from core.models import Products



User = get_user_model()

class Review(models.Model):
    """
    Modelo que representa a una reseña efectuada por un usuario a un producto
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario que realizo el review")
    title = models.CharField(max_length=150,null=True, help_text="Titulo del review")
    content = models.TextField(max_length=1000, help_text="Cuerpo del review")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="reviews", help_text="Producto al que pertenece el review")
    score = models.IntegerField(default=0, help_text="Puntuacion dada por el usuario a la calidad del producto")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de creacion del review")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha en que se actualiza el review")

    def __str__(self):
        return f"{self.user.email} - {self.title}"
    class Meta:
        ordering = ["-created_at"]