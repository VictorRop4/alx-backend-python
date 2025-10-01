from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserRole(models.TextChoices):
    GUEST = "guest", "Guest"
    HOST = "host", "Host"
    ADMIN = "admin", "Admin"

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable= False)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, null=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User,related_name="conversations")

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    sender_id = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name="sent_message")
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    
    def __str__(self):
        return f"Message {self.message_id}"