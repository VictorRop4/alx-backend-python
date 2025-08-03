from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import UnreadMessageViewSet

router = DefaultRouter()
router.register(r'unread-messages', UnreadMessageViewSet, basename='unread-messages')

urlpatterns = router.urls


urlpatterns = [
    path('delete-account/', views.delete_user, name='delete_user'),
]
