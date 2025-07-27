from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role']

# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    message_preview = serializers.CharField(source='content', read_only=True)  # Explicit CharField

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'conversation', 'content', 'timestamp', 'message_preview']
        read_only_fields = ['sender_name', 'timestamp', 'message_preview']

    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username


# --- Conversation Serializer with nested messages ---
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'conversation_id', 'participants', 'messages', 'created_at']

    # Example validation (if needed)
    def validate(self, attrs):
        if not attrs.get('participants'):
            raise serializers.ValidationError("Conversation must have at least one participant.")
        return attrs
