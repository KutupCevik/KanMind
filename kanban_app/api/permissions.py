from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    """
    Zugriff auf Boards wenn der Benutzer Mitglied oder Owner ist
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            user == obj.owner or obj.members.filter(id=user.id).exists()
        )


class IsBoardOwner(BasePermission):
    '''
    Zugriff nur für den Owner eines Boards
    '''
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user