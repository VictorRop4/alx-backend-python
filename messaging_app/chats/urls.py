from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested.routers import  NestedDefaultRouter


# Create a router instance
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name = 'token_obatain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refres'),
]
