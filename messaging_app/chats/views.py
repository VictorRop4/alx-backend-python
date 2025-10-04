from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer,UserSerializer
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .permissions import IsParticipantOfConversation
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

class MeView(generics.RetrieveUpdateAPIView):
    """
    Allows authenticated users to view or update their own profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated,IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise permissions.PermissionDenied("HTTP_403_FORBIDDEN")
        serializer.save(sender=self.request.user)
    
    

