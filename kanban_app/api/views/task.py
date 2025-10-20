from rest_framework import generics
from kanban_app.models import Task
from kanban_app.api.serializers.task import TaskCreateSerializer


class TaskCreateView(generics.CreateAPIView):
    '''
    POST: Erstellt eine neue Task in einem Board.
    Nur Board-Mitglieder oder der Owner dürfen Tasks erstellen.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer