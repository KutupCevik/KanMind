from django.db import models
from django.contrib.auth.models import User




class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')  #Zugriff auf alle Boards, die dieser Benutzer besitzt
    members = models.ManyToManyField(User, through='BoardMember', related_name='boards')    #Zugriff auf alle Boards, in denen dieser Benutzer Mitglied ist
    #related_name-Werte sind dazu da, dass du vom Benutzer aus (also vom User-Objekt) auf die verknüpften Boards zugreifen kannst.
    #Ohne sie würdest es später zu Namenskonflikten kommen, weil beide Beziehungen (owner und members) auf dasselbe Modell User zeigen.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BoardMember(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    #https://docs.djangoproject.com/en/5.2/ref/models/options/#unique-together
    #Ein Benutzer könnte mehrmals als Member in demselben Board eingetragen werden
    #Deshalb unique_together. Die Kombination aus board und user darf nur einmal existieren
    class Meta:
        unique_together = ('board', 'user')


class Task(models.Model):
    #https://docs.djangoproject.com/en/5.2/ref/models/fields/#choices
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

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status =models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)    #auto_now_add=True: Wird nur einmal beim Erstellen gesetzt
    updated_at = models.DateTimeField(auto_now=True)    #auto_now=True: Wird bei jedem Speichern automatisch aktualisiert
    due_date = models.DateField(null=True, blank=True)  #null=True: das Feld darf in der Datenbank leer bleiben und blank=True: Im Formular darf das Feld leer übermittelt werden
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks') #wenn der assignee User gelöscht wird, wird das Feld leer
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='review_tasks')

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)