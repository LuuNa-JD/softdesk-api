from django.urls import path
from .views import (
    ProjectCreateView, ProjectListView, ProjectDetailView,
    IssueCreateView, IssueListView, IssueDetailView,
    CommentCreateView, CommentListView, CommentDetailView
)

urlpatterns = [
    # Gestion des projets
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    # Gestion des issues
    path(
        '<int:project_id>/issues/create/',
        IssueCreateView.as_view(),
        name='issue-create'
    ),
    path('<int:project_id>/issues/', IssueListView.as_view(), name='issue-list'),
    path(
        '<int:project_id>/issues/<int:pk>/',
        IssueDetailView.as_view(),
        name='issue-detail'
    ),

    # Gestion des commentaires
    path(
        '<int:project_id>/issues/<int:issue_id>/comments/create/',
        CommentCreateView.as_view(),
        name='comment-create'
    ),
    path(
        '<int:project_id>/issues/<int:issue_id>/comments/',
        CommentListView.as_view(),
        name='comment-list'
    ),
    path(
        '<int:project_id>/issues/<int:issue_id>/comments/<uuid:pk>/',
        CommentDetailView.as_view(),
        name='comment-detail'
    ),
]
