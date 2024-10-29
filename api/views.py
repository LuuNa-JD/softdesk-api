from rest_framework import generics, permissions
from .models import Project, Issue
from users.models import Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from .permissions import IsContributor, IsCreator
from rest_framework.exceptions import ValidationError
from .models import Comment
from django.db import models


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Créer le projet et l'attribuer au propriétaire
        project = serializer.save(owner=self.request.user)
        # Ajouter le propriétaire en tant que contributeur
        Contributor.objects.create(user=self.request.user, project=project)


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Obtenir les projets uniquement si l'utilisateur est propriétaire ou contributeur
        return Project.objects.filter(
            models.Q(owner=self.request.user) |
            models.Q(contributors__user=self.request.user)
        ).distinct().order_by('-created_time')


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('contributors')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsCreator]


class IssueCreateView(generics.CreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_project(self):
        return Project.objects.get(pk=self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = self.get_project()
        # Récupérer le contributeur lié à l'utilisateur et au projet
        try:
            contributor = Contributor.objects.get(user=self.request.user, project=project)
        except Contributor.DoesNotExist:
            raise ValidationError("L'utilisateur n'est pas contributeur de ce projet.")

        # Sauvegarder l'issue avec le créateur et le projet spécifiés
        serializer.save(project=project, creator=contributor)


class IssueListView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        project = Project.objects.get(pk=self.kwargs['project_id'])
        return Issue.objects.filter(project=project).order_by('-created_time')


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsCreator]


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_issue(self):
        return Issue.objects.get(pk=self.kwargs['issue_id'])

    def perform_create(self, serializer):
        issue = self.get_issue()
        contributor = self.request.user.contributions.get(project=issue.project)  # Vérifie que l'utilisateur est un contributeur
        serializer.save(issue=issue, creator=contributor)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        issue = Issue.objects.get(pk=self.kwargs['issue_id'])
        return Comment.objects.filter(issue=issue).order_by('-created_time')


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsCreator]
