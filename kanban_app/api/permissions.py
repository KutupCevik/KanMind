# Third-party
from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    """
    Access to boards if the user is a member or the owner
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, 'owner') and hasattr(obj, 'members'):
            return obj.owner == user or obj.members.filter(id=user.id).exists()

        if hasattr(obj, 'board'):
            board = obj.board
            return board.owner == user or board.members.filter(id=user.id).exists()

        return False


class IsBoardOwner(BasePermission):
    """
    Access restricted to the board owner only
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allows deletion only for the task creator or the board owner."""
    def has_object_permission(self, request, view, obj):
        return (
            obj.created_by == request.user or
            obj.board.owner == request.user
        )


class IsCommentAuthor(BasePermission):
    """Allows deletion only for the comment author."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user