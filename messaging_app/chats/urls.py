from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Initialize the router
router = routers.DefaultRouter()

# Register viewsets
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include the router-generated URL patterns
urlpatterns = [
    path('', include(router.urls)),
]

