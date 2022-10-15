from django.db import models
from django.utils.timezone import now
from core.models.media import Media
from core.models.category import Category
from django.utils.text import slugify




class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to="uploads/")
    description = models.CharField(max_length=500, null=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self", related_name="parent_store", null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)}"
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.name