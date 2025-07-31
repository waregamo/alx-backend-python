from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

    def test_message_creation_triggers_notification(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        self.assertEqual(Notification.objects.filter(user=self.user2, message=msg).count(), 1)

    def test_message_edit_logs_history(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="First")
        msg.content = "Updated"
        msg.save()
        self.assertEqual(msg.edited, True)
        self.assertEqual(MessageHistory.objects.filter(message=msg).count(), 1)