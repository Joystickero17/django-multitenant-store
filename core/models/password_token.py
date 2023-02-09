from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class PasswordToken(models.Model):
    token=models.UUIDField(default=uuid.uuid4())
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=now())

    @property
    def still_valid(self):
        print("segundos del token", (now()-self.created_at).seconds)
        return (now()-self.created_at).seconds <= 3*60

