# Third-party
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Lokale Module
from kanban_app.models import Comment, Task
from kanban_app.api.serializers.comment import CommentSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner


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
