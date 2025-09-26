
from rest_framework.permissions import BasePermission

class IsOwnerOrParticipant(BasePermission):
    """
    Allow access only if the requesting user is the owner/participant
    of the conversation or message.
    """

    def has_object_permission(self, request, view, obj):
        # If obj is a Message, check conversation participants
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        
        # If obj is a Conversation, check participants directly
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        return False
