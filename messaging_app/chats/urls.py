from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router instance
router = DefaultRouter()

# Register your viewsets with the router
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),   # expose them at base of chats/
    path('token/', TokenObtainPairView.as_view(), name = 'token_obatain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refres'),
]
