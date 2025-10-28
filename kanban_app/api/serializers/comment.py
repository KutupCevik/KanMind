from rest_framework import serializers
from kanban_app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for comments (GET / POST).'''
    author = serializers.CharField(source='author.first_name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']