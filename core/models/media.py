from django.db import models
from django.utils.timezone import now

class Media(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="media/")
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return self.name