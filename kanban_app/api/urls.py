from django.urls import path
from kanban_app.api.views.board import BoardListView

urlpatterns = [
    path('boards/', BoardListView.as_view(), name='board-list'),
]