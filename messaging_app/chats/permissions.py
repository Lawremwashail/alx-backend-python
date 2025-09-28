from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants of a conversation can view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Require authentication first
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is a participant.
        Works for both Conversation and Message objects.
        """
        if hasattr(obj, "participants"):  # Conversation instance
            return request.user in obj.participants.all()
        if hasattr(obj, "conversation"):  # Message instance
            return request.user in obj.conversation.participants.all()
        return False

