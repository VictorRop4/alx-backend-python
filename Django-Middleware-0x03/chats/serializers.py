from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(max_length=500)
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'sender_username', 'message_body', 'sent_at', 'conversation']

    def get_sender_username(self, obj):
        return obj.sender_id.username

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )
    participant_names = serializers.SerializerMethodField()
    # ✅ Nested relationship for messages
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'created_at', 'participants', 'participant_names', 'messages']

    def get_participant_names(self, obj):
        return [user.username for user in obj.participants.all()]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
