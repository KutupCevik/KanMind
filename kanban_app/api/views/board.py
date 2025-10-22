# Third-party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Lokale Module
from kanban_app.models import Board
from kanban_app.api.serializers.board import BoardListSerializer, BoardCreateSerializer, BoardDetailSerializer, BoardUpdateSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner, IsBoardOwner


class BoardListCreateView(generics.ListCreateAPIView):
    '''
    GET  /api/boards/: Zeigt alle Boards, bei denen der Benutzer beteiligt ist.
    POST /api/boards/: Erstellt ein neues Board, setzt den Benutzer als Owner.
    '''
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        board = serializer.instance
        response_serializer = BoardListSerializer(board)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class BoardDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    '''
    GET     /api/boards/{board_id}/: Zeigt Board mit Members und Tasks.
    PATCH   /api/boards/{board_id}/: Aktualisiert Titel und Mitgliederliste.
    DELETE  /api/boards/{board_id}/: Board löschen (nur Owner).
    '''
    queryset = Board.objects.all()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()
        self.perform_destroy(board)
        return Response(status=status.HTTP_204_NO_CONTENT)