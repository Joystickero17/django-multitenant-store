from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()


class ExportFile(models.Model):
    file = models.FileField(upload_to="exports/")
    created_at = models.DateTimeField(auto_now_add=now)
    filename = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering= ["-created_at"]