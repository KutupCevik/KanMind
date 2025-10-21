from rest_framework import generics
from kanban_app.models import Task
from kanban_app.api.serializers.task import TaskCreateSerializer, TaskUpdateSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner
from rest_framework.permissions import IsAuthenticated


class TaskCreateView(generics.CreateAPIView):
    '''
    POST: Erstellt eine neue Task in einem Board.
    Nur Board-Mitglieder oder der Owner dürfen Tasks erstellen.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskUpdateView(generics.UpdateAPIView):
    '''
    PATCH: Aktualisiert eine bestehende Task.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]