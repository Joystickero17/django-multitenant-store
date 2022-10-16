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
    name = models.CharField(max_length=255)
    product_slug = models.SlugField(unique=True, null=True)
    quantity = models.PositiveBigIntegerField()
    brand = models.ForeignKey(Brand, null=True, related_name="products",help_text="Marca del producto, si es null se entendera como generica",on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, related_name="products", null=True)
    photos = models.ManyToManyField(Media)
    description = models.TextField(max_length=800, null=True)
    thumbnail = models.ImageField(upload_to="media/")
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)
    condition = models.CharField(max_length=50, choices=ConditionChoices.CHOICES, default=ConditionChoices.NEW)
    store = models.ForeignKey(to=Store, help_text="Tienda que publico el producto",on_delete=models.CASCADE, related_name="products")
    price = models.FloatField(null=True, help_text="si es null se marcara como gratuito")
    product_type = models.CharField(max_length=100, help_text="determina si un bien es un producto o un servicio, solo los servicios pueden llevar price=null", choices=ProductTypeChoices.CHOICES, default=ProductTypeChoices.SERVICE)
    discount = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs) -> None:
        if self.product_slug: 
            return super().save(*args, **kwargs)
        self.product_slug = f"{slugify(self.name)}{round(now().timestamp())}"
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