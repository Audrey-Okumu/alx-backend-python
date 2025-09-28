from rest_framework import serializers
from .models import User, Conversation, Message


# -------------------------------
# User Serializer
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']


# -------------------------------
# Message Serializer
# -------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested user
    message_body = serializers.CharField(max_length=2000)  # Explicit CharField

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# -------------------------------
# Conversation Serializer
# -------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()  # Custom computed field

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'message_count', 'created_at']

    def get_message_count(self, obj):
        # Return total number of messages in this conversation
        return obj.messages.count()
    
    def validate(self, data):
        # Example validation: ensure at least 2 participants
        if obj := getattr(self, 'instance', None):
            if obj.participants.count() < 2:
                raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return data
