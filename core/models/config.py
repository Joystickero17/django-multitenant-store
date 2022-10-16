from django.db import models



class Config(models.Model):
    main_color = models.CharField(max_length=100, null=True, help_text="Color principal con el que se caracteriza la tienda")
    secondary_color = models.CharField(max_length=100, null=True, help_text="Color secundario con el que se caracteriza la tienda")