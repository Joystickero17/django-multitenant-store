from django.db import models
from django.utils.timezone import now



class Category(models.Model):
    """
    Modelo que representa la categoria de un producto o una empresa.
    """
    name = models.CharField(max_length=255, help_text="Nombre de la categoria")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de creacion de la categoria")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de modificacion del la categoria")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, help_text="categoria padre de esta categoria")
    def __str__(self):
        return self.name