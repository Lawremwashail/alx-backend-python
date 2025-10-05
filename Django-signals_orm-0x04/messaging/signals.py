from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving, if the message already exists and the content changes,
    log the old content into MessageHistory.
    """
    if not instance.pk:
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content has changed
    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content
        )
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Clean up all related data when a User is deleted.
    """
    # Delete all messages where the user was sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications related to this user
    Notification.objects.filter(user=instance).delete()

    # Delete all message histories where edited_by is this user
    MessageHistory.objects.filter(edited_by=instance).delete()
