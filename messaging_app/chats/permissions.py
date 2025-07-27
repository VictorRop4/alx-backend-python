from rest_framework.permissions import BasePermission

class IsParticipantOrSender(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'sender'):
            return request.user == obj.sender or request.user in obj.conversation.participants.all()
        return False
