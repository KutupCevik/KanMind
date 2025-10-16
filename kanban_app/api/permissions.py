from rest_framework.permissions import BasePermission


# Zugriff auf Boards wenn der Benutzer Mitglied oder Owner ist.
class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            user == obj.owner or obj.members.filter(id=user.id).exists()
        )