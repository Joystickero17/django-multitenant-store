from django.contrib.auth import get_user_model
from django.db import models
from core.choices.model_choices import PersonType, DocumentType

User = get_user_model()


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    person_type = models.CharField(max_length=30, choices=PersonType.CHOICES)
    document_type = models.CharField(max_length=50, choices=DocumentType.CHOICES)
    document_number = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Client(Person):
    pass

class StoreOwner(Person):
    pass

class Employee(Person):
    pass
