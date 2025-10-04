from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants can access a conversation or its messages.
    """
    def has_object_permission(self, request, view):
            return bool(request.user and request.user.Isauthenticated)
    
    def has_object_permission(self, request, view, obj):
        # Step 2: Allow access only if the user is a participant
        if hasattr(obj, "participants"):  # Conversation instance
            return obj.participants.filter(id=request.user.id).exists()

        if hasattr(obj, "conversation"):  # Message instance
            return obj.conversation.participants.filter(id=request.user.id).exists()

        return False

