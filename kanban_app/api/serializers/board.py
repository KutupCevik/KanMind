# Standardbibliothek
# (keine)

# Third-party
from rest_framework import serializers
from django.contrib.auth.models import User

# Lokale Module
from kanban_app.models import Board, BoardMember, Task, Comment
from django.db.models import Count


"""Serializer für Board-Übersicht (GET /api/boards/)."""
class BoardListSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id',
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


"""Serializer für Board-Erstellung (POST /api/boards/)"""
class BoardCreateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Board
        fields = ['id', 'title', 'members']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        board.members.add(*members)
        return board


class MemberSerializer(serializers.ModelSerializer):
    '''Für Board-Mitglieder'''
    fullname = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskListSerializer(serializers.ModelSerializer):
    '''Für Tasks im Board-Detail'''
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]


'''Serializer für Board-Detail (GET /api/boards/{id}/)'''
class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True, source='tasks.all')

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']