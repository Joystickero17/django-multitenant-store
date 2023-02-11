from django.db import models
from django.utils.timezone import now
from core.models.config import Config
from core.models.media import Media
from core.models.category import Category
from django.utils.text import slugify
from core.utils.model_choices import CompanyEmployeeChoices
from django.conf import settings
from django.urls import reverse




class Store(models.Model):
    """
    Modelo que referencia a una tienda dentro del sistema
    """
    name = models.CharField(max_length=255, help_text="Nombre de la tienda")
    slug = models.SlugField(max_length=200, unique=True, help_text="sufijo para ubicar la tienda facilmente por URL")
    logo = models.ImageField(upload_to="uploads/", null=True, help_text="imagen que contiene el logotipo de la empresa")
    description = models.CharField(max_length=500, null=True, help_text="Una breve descripcion de la Empresa")
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, help_text="Categoria principal a la que se dedica la empresa")
    parent = models.ForeignKey("self", related_name="parent_store", null=True, on_delete=models.CASCADE, help_text="Referencia a una tienda padre que la haya referenciado o en caso de ser franquicia, la empresa matriz")
    created_at = models.DateTimeField(auto_now_add=now, help_text="Fecha de ingreso al sistema")
    updated_at = models.DateTimeField(auto_now=now, help_text="Fecha de actualizacion de la informacion")
    config = models.OneToOneField(Config, on_delete=models.CASCADE, null=True, help_text="relacion con confoguracion de la Empresa")
    bussiness_legal_id = models.CharField(unique=True, null=True, max_length=255, help_text="Numero de Identificacion Comercial de la empresa, varia dependiendo del pais, EJ: Venezuela, RIF.")
    money = models.FloatField(default=0, help_text="Dinero por retirar de la tienda")
    company_employee_number = models.CharField(choices=CompanyEmployeeChoices.CHOICES, max_length=255, help_text="Numero estimado de empleados de la Empresa.")
    company_anual_income = models.FloatField(null=True, help_text="Ingreso Anual de la empresa Expresado en Dolares, Campo no Obligatorio")

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)}"
        return super().save(*args, **kwargs)

    @property
    def store_url(self):
        return f"{settings.BASE_URL}{reverse('store_list', args=(self.slug,))}"

    def __str__(self):
        return self.name
