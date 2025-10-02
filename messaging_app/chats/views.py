from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends=[filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username', 'participants__email']  # search by user
    ordering_fields = ['created_at']

    def get_queryset(self):
        # List and lookup only conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get("participants", [])
        if not participants_ids:
            return Response({"error": "Participants are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch User instances to avoid invalid IDs and to ensure integrity
        participants = User.objects.filter(id__in=participants_ids)
        if not participants.exists():
            return Response({"error": "No valid participants found"},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        # ensure creator is included
        conversation.participants.add(request.user)
        conversation.participants.add(*participants)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        # object permission already verified, but re-check for clarity
        if request.user not in conversation.participants.all():
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        body = request.data.get("message_body")
        if not body:
            return Response({"error": "Message body is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=body
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends =[filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender_id__username']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Only messages whose conversation includes the user
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Save the authenticated user as the sender
        serializer.save(sender=self.request.user)
