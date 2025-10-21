from django.urls import path
from kanban_app.api.views.board import BoardListCreateView, BoardDetailUpdateDeleteView
from kanban_app.api.views.task import TaskCreateView, TaskUpdateDeleteView, TasksAssignedToMeView
from kanban_app.api.views.comment import CommentListCreateView, CommentDeleteView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetailUpdateDeleteView.as_view(), name='board-detail'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskUpdateDeleteView.as_view(), name='task-update-delete'),
    path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/<int:task_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('tasks/<int:task_id>/comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]