from django.db import models

class TenantModelMixin(models.Model):
    name = models.CharField(max_length=100)
    domain_prefix = models.CharField(max_length=100)


class TenantAwareModel(models.Model):
    """
    Clase Abstracta que referencia a la estructura del tenant
    """
    tenant = models.ForeignKey(TenantModelMixin, on_delete=models.CASCADE)
    class Meta:
        abstract = True