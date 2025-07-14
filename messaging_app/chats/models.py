from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Extend AbstractUser to allow custom user fields
class User(AbstractUser):
    # Add extra fields here if needed, e.g., phone_number, profile_picture, etc.
    pass


# Conversation model representing a chat between multiple users
class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# Message model for messages within a conversation
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
