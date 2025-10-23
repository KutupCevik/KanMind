# Third-party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

# Lokale Module
from kanban_app.models import Comment, Task
from kanban_app.api.serializers.comment import CommentSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner, IsCommentAuthor


class CommentListCreateView(generics.ListCreateAPIView):
    '''
    GET: Listet alle Kommentare einer Task.
    POST: Erstellt neuen Kommentar.
    Nur Board-Member oder Owner dürfen zugreifen.
    '''
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

        # Zugriff prüfen
        if not (board.owner == user or board.members.filter(id=user.id).exists()):
            raise PermissionDenied('Du bist kein Mitglied dieses Boards.')

        return Comment.objects.filter(task=task).order_by('created_at')

    def perform_create(self, serializer):
        task = self.get_task()
        user = self.request.user
        board = task.board

        # Zugriff prüfen
        if not (board.owner == user or board.members.filter(id=user.id).exists()):
            raise PermissionDenied('Du bist kein Mitglied dieses Boards.')

        serializer.save(author=user, task=task)


class CommentDeleteView(generics.DestroyAPIView):
    '''
    DELETE: Löscht einen Kommentar.
    Nur der Autor darf löschen.
    '''
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
