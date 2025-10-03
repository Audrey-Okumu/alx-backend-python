from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return unread messages for a specific user.
        Uses `.only()` to optimize query by fetching only needed fields.
        """
        return (
            super().get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )
