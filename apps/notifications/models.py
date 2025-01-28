from django.db import models
from utils.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

class NotificationLog(BaseModel):
    message = models.TextField()
    recipient = models.ForeignKey(to=User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('notification'),)
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.recipient} - {self.sent_at}"
