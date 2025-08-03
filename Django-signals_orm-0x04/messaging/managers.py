from django.db import models
from django.conf import settings

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        )