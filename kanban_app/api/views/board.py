# Third-party
from rest_framework import generics, status
from rest_framework.response import Response

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
        owned = Board.objects.filter(owner=user)
        member = Board.objects.filter(members=user)
        return (owned | member).distinct()

    def get_serializer_class(self):
        return BoardCreateSerializer if self.request.method == 'POST' else BoardListSerializer

    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        serializer_context['request'] = self.request
        return serializer_context
    
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