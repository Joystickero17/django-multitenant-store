from django.contrib.auth import get_user_model
from django.db import models
from core.choices.model_choices import PersonType, DocumentType
from .store import Store

User = get_user_model()


class Info(models.Model):
    """
    Modelo de relacion Uno a Uno para guardar informacion adicional del usuario
    """
    person_type = models.CharField(max_length=30, choices=PersonType.CHOICES, help_text="Tipo de persona para saber si es una empresa o una persona natural")
    document_type = models.CharField(max_length=50, choices=DocumentType.CHOICES, help_text="Tipo de documento, si es RIF o cedula")
    document_number = models.CharField(max_length=100, help_text="Numero de identificacion del documento", unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info", help_text="Usuario al que pertenece la informacion")
