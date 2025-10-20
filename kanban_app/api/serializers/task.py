from rest_framework import serializers
from kanban_app.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    '''Serializer für das Erstellen einer neuen Task (POST /api/tasks/).'''

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]