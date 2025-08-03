# messaging/serializers.py
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender']
        read_only_fields = ['sender']
