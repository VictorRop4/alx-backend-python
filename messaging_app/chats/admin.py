from django.contrib import admin

from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Conversation, Message

# Get the custom user model (or default one if not customized)
User = get_user_model()

# Register the user model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active']
    search_fields = ['username', 'email']

# Register the Conversation model
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation_id', 'created_at']
    search_fields = ['conversation_id']
    filter_horizontal = ['participants']

# Register the Message model
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'content', 'timestamp']
    list_filter = ['conversation', 'timestamp']
    search_fields = ['content', 'sender__username']
