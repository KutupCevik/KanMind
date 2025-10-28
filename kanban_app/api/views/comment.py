# Third-party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError

# Lokale Module
from kanban_app.models import Comment, Task
from kanban_app.api.serializers.comment import CommentSerializer
from kanban_app.api.permissions import IsCommentAuthor


class CommentListCreateView(generics.ListCreateAPIView):
    """
    GET: Lists all comments for a task.
    POST: Creates a new comment.
    Only board members or the owner are allowed to access.
    """
    serializer_class = CommentSerializer

    def get_task(self):
        task_id = self.kwargs['task_id']
        try:
            return Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound('Task nicht gefunden.')

    def get_queryset(self):
        task = self.get_task()
        user = self.request.user
        board = task.board

        if not (board.owner == user or board.members.filter(id=user.id).exists()):
            raise PermissionDenied('Du bist kein Mitglied dieses Boards.')

        return Comment.objects.filter(task=task).order_by('created_at')

    def perform_create(self, serializer):
        task = self.get_task()
        user = self.request.user
        board = task.board

        if not (board.owner == user or board.members.filter(id=user.id).exists()):
            raise PermissionDenied('Du bist kein Mitglied dieses Boards.')

        serializer.save(author=user, task=task)


class CommentDeleteView(generics.DestroyAPIView):
    """
    DELETE: Deletes a comment.
    Only the author is allowed to delete.
    """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('pk')
        if not (task_id.isdigit() and comment_id.isdigit()):
            raise ValidationError('Ungültige ID.')
        return super().get_object()
