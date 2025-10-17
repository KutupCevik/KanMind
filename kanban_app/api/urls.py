from django.urls import path
from kanban_app.api.views.board import BoardListCreateView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
]