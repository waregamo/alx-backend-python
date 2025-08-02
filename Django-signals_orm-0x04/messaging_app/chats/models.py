from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings

# 1. Custom User model
class User(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('moderator', 'Moderator'),
    )

    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.username} ({self.role})"


# 2. Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# 3. Message model
class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in Conversation {self.conversation.conversation_id}"
