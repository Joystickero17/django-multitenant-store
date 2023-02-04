from django.core.management import BaseCommand
from core.models.gc_model import GiftCard
import uuid


class Command(BaseCommand):
    def handle(self, *args, **options):
        gcs = [
            GiftCard(code=str(uuid.uuid4())[-5:])
            for item in range(50)
        ]
        GiftCard.objects.bulk_create(gcs)