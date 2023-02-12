from django.db import models
from core.models.store import Store
from core.choices.model_choices import ProductStorageChoices


class ProductStorage(models.Model):
    """
    Modelo para el almacen de las tiendas
    al igual que las direcciones, se puede 
    tener varios almacenes, de tipo
    - Tienda Fisica
    - Almacen
    """
    storage_type = models.CharField(max_length=255, choices=ProductStorageChoices.CHOICES, default=ProductStorageChoices.TIENDA_FISICA)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    region = models.CharField(max_length=255, null=True, blank=True)
    subregion = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    coordinate_x = models.FloatField(default=0)
    coordinate_y = models.FloatField(default=0)
    zoom = models.FloatField(default=0)