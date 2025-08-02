from rest_framework import permissions

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to ensure:
    - Only authenticated users can access the API.
    - Only conversation participants can send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only allow access to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) if the user is a participant
        if request.method in permissions.SAFE_METHODS:
            return request.user in [obj.sender, obj.receiver]

        # Allow modifying methods (PUT, PATCH, DELETE) only for participants
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in [obj.sender, obj.receiver]

        # For other methods like POST
        return request.user in [obj.sender, obj.receiver]

