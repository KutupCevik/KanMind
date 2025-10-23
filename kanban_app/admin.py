from django.contrib import admin
from .models import Board, BoardMember, Task


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    search_fields = ('title', 'owner__username', 'owner__email')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'board', 'created_by')