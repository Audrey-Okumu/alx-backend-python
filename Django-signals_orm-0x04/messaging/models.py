from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="edited_messages"
    )

    # new field for threaded replies
    parent_message = models.ForeignKey(
        'self',                # self-referential relationship
        null=True, blank=True, # root messages will have no parent
        on_delete=models.CASCADE,
        related_name="replies"
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

    class Meta:
        ordering = ["timestamp"]

    # helper method to fetch replies recursively
    def get_thread(self):
        thread = {
            "id": self.id,
            "content": self.content,
            "sender": self.sender.username,
            "timestamp": self.timestamp,
            "replies": []
        }
        for reply in self.replies.all():   # thanks to related_name="replies"
            thread["replies"].append(reply.get_thread())
        return thread


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
