from django.db import models
from django.utils.timezone import now

class Media(models.Model):
    """
    Modelo para representar archivos multimedia que pertenezca a alguna entidad del sistema
    """
    name = models.CharField(max_length=255, help_text="Nombre del archivo")
    file = models.FileField(upload_to="media/", help_text="Ruta relativa del archivo")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de subida del documento")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de modificacion")

    def __str__(self):
        return self.name