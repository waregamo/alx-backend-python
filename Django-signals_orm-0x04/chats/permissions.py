from rest_framework import permissions

 # return request.user in obj.participants.all()
class IsParticipantOfConversation(permissions.BasePermission):
    message = "You are not a participant of this conversation."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.participants.all()
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.all()
        return False