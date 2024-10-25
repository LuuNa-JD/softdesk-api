from django.urls import path
from .views import ProjectCreateView, ProjectDetailView, IssueCreateView, CommentCreateView, ProjectListView, IssueDetailView, CommentDetailView, IssueListView, CommentListView

urlpatterns = [
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/issues/create/', IssueCreateView.as_view(), name='issue-create'),
    path('projects/<int:project_id>/issues/', IssueListView.as_view(), name='issue-list'),
    path('projects/<int:project_id>/issues/<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/create/', CommentCreateView.as_view(), name='create-comment'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<uuid:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
