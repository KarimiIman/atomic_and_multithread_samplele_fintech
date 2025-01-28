from apps.notifications.models import NotificationLog
from django.db import transaction
import logging

logger = logging.getLogger('custom')


class NotificationService:
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message

    def send_notification(self):
        self._save_notification()
        self._send_notification()

    def _save_notification(self):
        with transaction.atomic():
            NotificationLog.objects.create(
                recipient=self.recipient,
                message=self.message,
            )

    def _send_notification(self):
        logger.info(f"send notif : message : {self.message} for {self.recipient}")
        print(f"{self.recipient.username}: {self.message}")
