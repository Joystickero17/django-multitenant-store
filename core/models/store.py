from django.db import models
from django.utils.timezone import now
from core.models.media import Media
from core.models.category import Category




class Store(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="uploads/")
    description = models.CharField(max_length=500, null=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self", related_name="parent_store", null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return self.name