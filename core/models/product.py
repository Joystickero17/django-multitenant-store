from uuid import uuid4
from django.db import models
from core.models.brand import Brand
from core.models.category import Category
from django.utils.text import slugify
from core.models.store import Store
from .media import Media, now
from django.utils.timezone import now

class ProductTypeChoices:
    SERVICE = "SERVICE"
    MERCHANDISE = "MERCHANDISE"
    CHOICES = [
        (SERVICE, "SERVICIOS"),
        (MERCHANDISE, "MERCANCIA")
    ]
class ConditionChoices:
    NEW = "NEW"
    USED = "USED"
    REFURBISHED = "REFURBISHED"
    CHOICES = [
        (NEW, "Nuevo"),
        (USED, "Usado"),
        (REFURBISHED, "Remanufacturado")
    ]
class Products(models.Model):
    """
    Modelo que representa a los productos que se almacenan en la base de datos
    """
    name = models.CharField(max_length=255, help_text="Nombre o título del producto")
    product_slug = models.SlugField(unique=True, null=True, help_text="sufijo unico para encontrar el producto por la URL")
    quantity = models.PositiveBigIntegerField(help_text="Cantidad del producto en inventario")
    brand = models.ForeignKey(Brand, null=True, related_name="products",help_text="Marca del producto, si es null se entendera como generica",on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, help_text="Categoria del producto",on_delete=models.SET_NULL, related_name="products", null=True)
    photos = models.ManyToManyField(Media, help_text="Fotos y/o archivos asociados al producto")
    description = models.TextField(max_length=800, null=True, help_text="Descripcion corta del producto")
    large_description = models.TextField(max_length=5000, null=True, help_text="Descripcion larga del producto del producto")
    thumbnail = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, related_name="main_products",help_text="Miniatura del producto")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de creacion del producto")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de actualizacion del producto")
    condition = models.CharField(max_length=50, choices=ConditionChoices.CHOICES, default=ConditionChoices.NEW, help_text="Condicion del producto")
    store = models.ForeignKey(to=Store, help_text="Tienda que publico el producto",on_delete=models.CASCADE, related_name="products")
    price = models.FloatField(null=True, help_text="si es null se marcara como gratuito")
    product_type = models.CharField(max_length=100, help_text="determina si un bien es un producto o un servicio, solo los servicios pueden llevar price=null", choices=ProductTypeChoices.CHOICES, default=ProductTypeChoices.SERVICE)
    discount = models.PositiveSmallIntegerField(default=0, help_text="Porcentaje de descuento de un producto, en caso de que lo tenga.")

    class Meta:
        ordering = ["-created_at"]
    def save(self, *args, **kwargs) -> None:
        if self.product_slug: 
            return super().save(*args, **kwargs)
        self.product_slug = f"{slugify(self.name)}{uuid4()}"
        print(self.product_slug)
        return super().save(*args, **kwargs)
    
    @property
    def get_discount(self):
        return self.price - self.price*self.discount/100 if self.discount else None

    @property
    def has_stock(self):
        return bool(self.quantity)

    @property
    def verbose_condition(self):
        return dict(ConditionChoices.CHOICES).get(self.condition)

    @property
    def rating(self):
        if not self.reviews.exists(): return 0
        return round(sum(self.reviews.all().values_list("score", flat=True))/self.reviews.all().count())
        
    def __str__(self):
        return self.name