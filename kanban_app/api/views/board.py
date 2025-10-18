# Third-party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Lokale Module
from kanban_app.models import Board
from kanban_app.api.serializers.board import BoardListSerializer, BoardCreateSerializer, BoardDetailSerializer, BoardUpdateSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner


'''
GET  /api/boards/: Zeigt alle Boards, bei denen der Benutzer beteiligt ist.
POST /api/boards/: Erstellt ein neues Board, setzt den Benutzer als Owner.
'''
class BoardListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        owned = Board.objects.filter(owner=user)
        member = Board.objects.filter(members=user)
        return (owned | member).distinct()

    def get_serializer_class(self):
        return BoardCreateSerializer if self.request.method == 'POST' else BoardListSerializer
    
    def perform_create(self, serializer):
        # Owner automatisch aus dem eingeloggten Benutzer setzen
        serializer.save(owner=self.request.user)


'''
GET     /api/boards/{board_id}/: Zeigt Board mit Members und Tasks.
PATCH   /api/boards/{board_id}/: Aktualisiert Titel und Mitgliederliste.
'''
class BoardDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer