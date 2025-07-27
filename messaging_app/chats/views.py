from rest_framework import viewsets, status, filters  # <-- 'filters' included here
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import AllowAny

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]  # <-- using filters here
    search_fields = ['participants__user_id']  # adjust to match your field

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]  # <-- using filters here
    ordering_fields = ['timestamp']  # ensure Message has this field

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        try:
            sender = User.objects.get(user_id=sender_id)
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except (User.DoesNotExist, Conversation.DoesNotExist):
            return Response({'error': 'Invalid sender or conversation ID'}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
