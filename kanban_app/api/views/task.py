# Third-party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# Lokale Module
from kanban_app.models import Task
from kanban_app.api.serializers.task import TaskCreateSerializer, TaskUpdateSerializer, TaskListSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner, IsTaskCreatorOrBoardOwner


class TaskCreateView(generics.CreateAPIView):
    '''
    POST: Erstellt eine neue Task in einem Board.
    Nur Board-Mitglieder oder der Owner dürfen Tasks erstellen.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    '''
    PATCH: Aktualisiert eine bestehende Task.
    DELETE: Löscht eine Task. Nur der Ersteller oder der Board-Owner darf löschen.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        self.perform_destroy(task)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk.isdigit():
            raise ValidationError('Ungültige Task-ID.')
        return super().get_object()


class TasksAssignedToMeView(generics.ListAPIView):
    '''
    GET: Gibt alle Tasks zurück, bei denen der Benutzer Assignee ist.
    '''
    serializer_class = TaskListSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class TasksReviewingView(generics.ListAPIView):
    '''
    GET: Gibt alle Tasks zurück, bei denen der Benutzer Reviewer ist.
    '''
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)