from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class SignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="pass")
        self.receiver = User.objects.create_user(username="bob", password="pass")

    def test_notification_created_on_message(self):
        # Create message
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello Bob!")

        # Check notification
        notif = Notification.objects.filter(user=self.receiver, message=msg).first()
        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)

