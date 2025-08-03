# messaging/managers.py

from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages where the given user is the receiver.
        Only selected fields are retrieved for performance.
        """
        return super().get_queryset().filter(
            receiver=user,
            read=False
        ).only('id', 'sender', 'timestamp', 'content')
