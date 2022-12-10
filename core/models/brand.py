from django.db import models
from django.utils.timezone import now



class Brand(models.Model):
    """
    Modelo que representa una marca en el sistema para un producto
    """
    name = models.CharField(max_length=255,help_text="Nombre de la marca")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de creacion de la marca")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de modificacion de datos")

    def __str__(self):
        return self.name
    
    @property
    def product_count(self) -> int:
        """
        Propiedad para contar los productos de la categoria
        """
        return self.products.all().count