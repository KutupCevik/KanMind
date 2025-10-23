from django.contrib import admin
from .models import Board, Task, Comment


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    search_fields = ('title', 'owner__username', 'owner__email')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'board', 'created_by')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'author')