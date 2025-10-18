from django.urls import path
from kanban_app.api.views.board import BoardListCreateView, BoardDetailUpdateDeleteView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetailUpdateDeleteView.as_view(), name='board-detail'),
]