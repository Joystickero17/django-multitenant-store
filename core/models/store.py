from django.db import models
from .tenant_mixin import TenantAwareModel
from django.utils.timezone import now



class Store(TenantAwareModel):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    child = models.ManyToManyField("self", related_name="child_store")
    parent = models.ForeignKey("self", related_name="parent_store", null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)