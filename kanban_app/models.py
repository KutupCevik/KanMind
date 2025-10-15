from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey()
    members = models.ManyToManyField()
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


class Comment(models.Model):
    pass