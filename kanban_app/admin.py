from django.contrib import admin
from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'created_at')
    search_fields = ('title', 'owner__username', 'owner__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)