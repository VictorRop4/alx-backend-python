from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants can access a conversation or its messages.
    """
    def has_object_permission(self, request, view):
            return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        # Step 2: Allow access only if the user is a participant
    
        if hasattr(obj, "participants"):        # Conversation instance
            conversation = obj
        elif hasattr(obj, "conversation"):      # Message instance
            conversation = obj.conversation
        else:
            return False

        # Allow only if the user is a participant
        is_participant = conversation.participants.filter(id=request.user.id).exists()

        # Apply restriction to view, send, update, and delete operations
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return is_participant

        # Deny all other unsafe or unsupported methods
        return False