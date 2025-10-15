from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, through='BoardMember', related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BoardMember(models.Model):
    board = models.ForeignKey()
    user = models.ForeignKey()
    added_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    # Quelle: https://docs.djangoproject.com/en/5.2/ref/models/fields/#choices
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    bord = models.ForeignKey()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status =models.CharField(max_length=20)
    priority = models.CharField(max_length=20)
    created_by = models.ForeignKey()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    due_date = models.DateField()
    assignee = models.ForeignKey()
    reviewer = models.ForeignKey()

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey()
    author = models.ForeignKey()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return