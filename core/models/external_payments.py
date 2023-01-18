from django.db import models
from django.utils.timezone import now
from core.utils.model_choices import PaymentMethodChoices,NationalBankChoices,ExternalPaymentStatus
from core.models.order import Order

class ExternalPayment(models.Model):
    """
    Modelo que sirve para guardar pagos secundarios de ordenes,
    tales como pagos moviles, o transferencias.
    """
    payment_id = models.CharField(unique=True, max_length=255)
    payment_type = models.CharField(choices=PaymentMethodChoices.CHOICES, max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="external_payments")
    national_bank = models.CharField(max_length=255, choices=NationalBankChoices.CHOICES, null=True)
    state = models.CharField(choices=ExternalPaymentStatus.CHOICES, max_length=255, default=ExternalPaymentStatus.REVIEW)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)