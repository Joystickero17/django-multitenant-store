from django.db import models
from core.models.store import Store



class ProductStorage(models.Model):
    """
    Modelo para el almacen de las tiendas
    al igual que las direcciones, se puede 
    tener varios almacenes.
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    region = models.CharField(max_length=255, null=True, blank=True)
    subregion = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    coordinates = models.CharField(max_length=255, null=True, blank=True)