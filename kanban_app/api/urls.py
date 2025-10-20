from django.urls import path
from kanban_app.api.views.board import BoardListCreateView, BoardDetailUpdateDeleteView
from kanban_app.api.views.task import TaskCreateView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetailUpdateDeleteView.as_view(), name='board-detail'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
]