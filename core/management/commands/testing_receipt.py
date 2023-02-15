import random
from django.core.management import BaseCommand
from core.models.order import Order,OrderStatusChoices
from core.controllers.receipt_controller import generate_receipt

class Command(BaseCommand):
    def handle(self, *args, **options):
        order = random.choice(Order.objects.filter(payment_status=OrderStatusChoices.PAYMENT_SUCCESS))
        data:bytes = generate_receipt(order)
        with open("test_receipt.pdf", "wb") as f:
            self.stdout.write(self.style.WARNING("Writing receipt"))
            f.write(data)
        self.stdout.write(self.style.SUCCESS("Receipt generated successfully"))