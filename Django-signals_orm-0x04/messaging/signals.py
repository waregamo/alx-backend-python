from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory  # Import your Message model

# The @receiver decorator connects this function to the post_save signal
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    This function is called every time a Message instance is saved.
    """
    # The 'created' boolean is True only on the first save (i.e., object creation)
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        
        if original_message.content != instance.content:
            editor = getattr(instance, 'editor', None)
            MessageHistory.objects.create(
                message=original_message,
                old_content = original_message.content,
                edited_by=editor
            )
            instance.edited = True
            instance.last_edited_by = editor

@receiver(post_delete, sender=User)
def clean_up_user(sender, instance, **kwargs):
    """
    When a user is deleted, this signal cleans up all their messages
    and notifications.
    """
    user = instance

    message_to_delete = Message.objects.filter(Q(sender=user) | Q(receiver=user))

    if message_to_delete.exists():
        message_to_delete.delete()
    notifications_to_delete = Notification.objects.filter(Q(user=user))
    if notifications_to_delete.exists():
        notifications_to_delete.delete()