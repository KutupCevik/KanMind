from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey()
    members = models.ManyToManyField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        pass


class BoardMember(models.Model):
    pass


class Task(models.Model):
    pass


class Comment(models.Model):
    pass