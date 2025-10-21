# Third-party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Lokale Module
from kanban_app.models import Comment, Task
from kanban_app.api.serializers.comment import CommentSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner, IsCommentAuthor


class CommentListCreateView(generics.ListCreateAPIView):
    '''
    GET: Listet alle Kommentare einer Task.
    POST: Erstellt einen neuen Kommentar.
    Nur Board-Mitglieder dürfen lesen und schreiben.
    '''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        task = Task.objects.get(pk=self.kwargs['task_id'])
        serializer.save(author=self.request.user, task=task)


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
