from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver = User.objects.create_user(username='bob', password='password456')

    def test_notification_created_on_new_message(self):
        # Ensure no notifications exist at the start
        self.assertEqual(Notification.objects.count(), 0)

        # Create a new message
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Bob!'
        )

        # Confirm that a Notification was created
        self.assertEqual(Notification.objects.count(), 1)

        # Check that the Notification is linked to the correct user and message
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, msg)
        self.assertFalse(notification.is_read)
