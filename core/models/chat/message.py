from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="sent_messages", on_delete=models.SET_NULL, null=True)
    to_user = models.ForeignKey(User, related_name="received_messages", on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        ordering = ["-created_at"]