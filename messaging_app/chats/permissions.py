# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Allow only authenticated users.
    - Allow only participants of a conversation to access its messages.
    """

    def has_permission(self, request, view):
        # General rule: must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If object is a Message → check conversation participants
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # If object is a Conversation → check participants directly
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False
