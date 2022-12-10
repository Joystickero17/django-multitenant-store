from django.db import models



class Config(models.Model):
    """
    Modelo para representar la configuracion de la tienda,aspecto de la misma.
    """
    main_color = models.CharField(max_length=100, null=True, help_text="Color principal con el que se caracteriza la tienda")
    secondary_color = models.CharField(max_length=100, null=True, help_text="Color secundario con el que se caracteriza la tienda")
    whatsapp_number = models.CharField(max_length=100,null=True, help_text="Numero que aparecera en el icono de whatsapp de la tienda")