from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from kanban_app.models import Board
from kanban_app.api.serializers.board import BoardListSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner


# Zeigt alle Boards, bei denen der Benutzer beteiligt ist.
# GET /api/boards/
class BoardListView(generics.ListAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            members=user
        ).union(    #https://docs.djangoproject.com/en/5.2/ref/models/querysets/#union
            Board.objects.filter(owner=user)
        ).distinct()    #https://docs.djangoproject.com/en/5.2/ref/models/querysets/#distinct