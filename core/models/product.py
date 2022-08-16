from .tenant_mixin import TenantAwareModel, models
from .media import Media, now


class Products(TenantAwareModel):
    name = models.CharField(max_length=255)
    quantity = models.PositiveBigIntegerField()
    category = models.CharField(max_length=255)
    media = models.ManyToManyField(Media)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)