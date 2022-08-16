from .tenant_mixin import TenantAwareModel, models
from django.utils.timezone import now

class Media(TenantAwareModel):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="media/")
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)