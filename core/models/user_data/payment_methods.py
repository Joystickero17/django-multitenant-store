from django.db import models
from core.utils.model_choices import PaymentMethodChoices, NationalBankChoices


class PaymentMethod(models.Model):
    type = models.CharField(choices=PaymentMethodChoices.CHOICES, max_length=255)
    account_number = models.CharField(null=True,blank=True,max_length=255)
    email_adress = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    national_bank = models.CharField(null=True,blank=True, choices=NationalBankChoices.CHOICES, max_length=255)