from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

#pre_save so we can grab the old content before it gets overwritten.
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # If this is an update (not a new message)
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # content has changed
                # Save old version to history
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                # Mark the message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass
