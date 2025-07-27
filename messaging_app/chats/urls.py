# chats/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Initialize the router
routers = DefaultRouter()

# Register viewsets
routers.register(r'conversations', ConversationViewSet, basename='conversation')
routers.register(r'messages', MessageViewSet, basename='message')

# Include the router-generated URL patterns
urlpatterns = [
    path('', include(routers.urls)),
]

