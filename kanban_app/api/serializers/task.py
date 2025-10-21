# Third-party
from rest_framework import serializers
from django.contrib.auth.models import User

# Lokale Module
from kanban_app.models import Task


class MemberSerializer(serializers.ModelSerializer):
    '''Kurzserializer für User (Assignee/Reviewer).'''
    fullname = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskCreateSerializer(serializers.ModelSerializer):
    '''Serializer für das Erstellen einer neuen Task (POST /api/tasks/).'''

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), required=False, allow_null=True
    )
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

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

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate_board(self, board):
        '''Prüfen, ob der Benutzer Mitglied des Boards ist.'''
        user = self.context['request'].user
        if not (board.owner == user or board.members.filter(id=user.id).exists()):
            raise serializers.ValidationError('Du bist kein Mitglied dieses Boards.')
        return board

    def validate(self, data):
        '''Assignee und Reviewer müssen Mitglieder desselben Boards sein.'''
        board = data.get('board')
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        for person in [assignee, reviewer]:
            if person and not board.members.filter(id=person.id).exists() and person != board.owner:
                raise serializers.ValidationError('Assignee oder Reviewer ist kein Mitglied des Boards.')
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        task = Task.objects.create(**validated_data)
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    '''Serializer für Task-Aktualisierung (PATCH /api/tasks/{id}/).'''
    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), required=False, allow_null=True
    )
    assignee = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'assignee',
            'reviewer',
            'due_date',
        ]

    def get_assignee(self, obj):
        if obj.assignee:
            return {
                'id': obj.assignee.id,
                'email': obj.assignee.email,
                'fullname': obj.assignee.first_name
            }
        return None

    def get_reviewer(self, obj):
        if obj.reviewer:
            return {
                'id': obj.reviewer.id,
                'email': obj.reviewer.email,
                'fullname': obj.reviewer.first_name
            }
        return None

    def validate(self, data):
        task = self.instance
        board = task.board
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        for person in [assignee, reviewer]:
            if person and not board.members.filter(id=person.id).exists() and person != board.owner:
                raise serializers.ValidationError('Assignee oder Reviewer ist kein Mitglied des Boards.')
        return data


class TaskListSerializer(serializers.ModelSerializer):
    '''Serializer für Task-Listen (Assigned-to-me / Reviewing).'''
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    board = serializers.IntegerField(source='bord.id')

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]
