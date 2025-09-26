# messaging_app/chats/permissions.py
from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants in a conversation can view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Global check: must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If checking a Conversation object
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If checking a Message object
        if isinstance(obj, Message):
            is_participant = request.user in obj.conversation.participants.all()

            # SAFE methods: just viewing → allowed if participant
            if request.method in permissions.SAFE_METHODS:
                return is_participant

            # UNSAFE methods: POST, PUT, PATCH, DELETE → still only participants
            if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                return is_participant

        return False
