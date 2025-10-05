
# chats/filters.py
import django_filters
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    sender = django_filters.NumberFilter(field_name='sender__id')
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']

class ConversationFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='participants__username', lookup_expr='icontains')
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Conversation
        fields = ['participant', 'start_date', 'end_date']