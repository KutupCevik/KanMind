# Third-party
from rest_framework import generics

# Lokale Module
from kanban_app.models import Board
from kanban_app.api.serializers.board import BoardListSerializer, BoardCreateSerializer

'''
GET  /api/boards/: Zeigt alle Boards, bei denen der Benutzer beteiligt ist.
POST /api/boards/: Erstellt ein neues Board, setzt den Benutzer als Owner.
'''
class BoardListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        return (
            Board.objects.filter(members=user)
            .union(Board.objects.filter(owner=user))    #https://docs.djangoproject.com/en/5.2/ref/models/querysets/#union
            .distinct() #https://docs.djangoproject.com/en/5.2/ref/models/querysets/#distinct
        )

    def get_serializer_class(self):
        return BoardCreateSerializer if self.request.method == 'POST' else BoardListSerializer

    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        serializer_context['request'] = self.request
        return serializer_context