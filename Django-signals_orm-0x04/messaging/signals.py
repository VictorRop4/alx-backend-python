from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.db.models import Q

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return  # Shouldn't occur, but safe guard

        if old_message.content != instance.content:
            # Save old content to MessageHistory
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )
            instance.edited = True  # Mark the message as edited

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # This step is technically redundant if on_delete=CASCADE is correctly used
    # But it ensures orphaned data like indirect logs or non-FK relations are removed

    # Delete all messages where user was sender or receiver (in case CASCADE missed something)
    Message.objects.filter(Q(sender=instance) | Q(receiver=instance)).delete()

    # Delete all MessageHistory entries where the message's sender was the user
    MessageHistory.objects.filter(message__sender=instance).delete()
  