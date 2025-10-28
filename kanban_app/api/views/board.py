# Third-party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Lokale Module
from kanban_app.models import Board
from kanban_app.api.serializers.board import BoardListSerializer, BoardCreateSerializer, BoardDetailSerializer, BoardUpdateSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner, IsBoardOwner


class BoardListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/boards/: Displays all boards the user is involved in.
    POST /api/boards/: Creates a new board and sets the user as the owner.
    """
    def get_queryset(self):
        user = self.request.user
        owned = Board.objects.filter(owner=user)
        member = Board.objects.filter(members=user)
        return (owned | member).distinct()

    def get_serializer_class(self):
        return BoardCreateSerializer if self.request.method == 'POST' else BoardListSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        board = serializer.instance
        response_serializer = BoardListSerializer(board)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class BoardDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET     /api/boards/{board_id}/: Displays a board with members and tasks.
    PATCH   /api/boards/{board_id}/: Updates the title and member list.
    DELETE  /api/boards/{board_id}/: Deletes the board (owner only).
    """
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