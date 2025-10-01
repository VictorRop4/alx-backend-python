from rest_framework import serializers
from .models import User, Message, Conversation

class  UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'phone_number', 'role', 'email','created_at']

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body','sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'created_at', 'participants','messages']