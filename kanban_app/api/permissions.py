# Third-party
from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    """
    Zugriff auf Boards wenn der Benutzer Mitglied oder Owner ist
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Wenn obj ein Board ist
        if hasattr(obj, 'owner') and hasattr(obj, 'members'):
            return obj.owner == user or obj.members.filter(id=user.id).exists()

        # Wenn obj eine Task ist
        if hasattr(obj, 'board'):
            board = obj.board
            return board.owner == user or board.members.filter(id=user.id).exists()

        return False


class IsBoardOwner(BasePermission):
    '''
    Zugriff nur für den Owner eines Boards
    '''
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsTaskCreatorOrBoardOwner(BasePermission):
    '''Erlaubt Löschen nur für den Task-Ersteller oder den Board-Owner.'''
    def has_object_permission(self, request, view, obj):
        return (
            obj.created_by == request.user or
            obj.board.owner == request.user
        )