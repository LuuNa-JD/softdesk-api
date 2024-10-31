from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db.models import Q
from .models import Project, Issue, Comment
from users.models import Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from .permissions import IsContributor, IsCreator


class ProjectCreateView(generics.CreateAPIView):
    """
    Vue pour la création d'un projet. Ajoute automatiquement l'utilisateur en tant que
    créateur et contributeur du projet.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Sauvegarde le projet avec l'utilisateur actuel comme créateur
        project = serializer.save(creator=self.request.user)
        # Ajoute l'utilisateur actuel en tant que contributeur du projet
        Contributor.objects.create(contributor=self.request.user, project=project)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = (
            "Projet créé avec succès ! Vous êtes ajouté comme propriétaire "
            "et contributeur."
        )
        return response


class ProjectListView(generics.ListAPIView):
    """
    Vue pour lister tous les projets auxquels l'utilisateur est associé, soit en tant
    que créateur soit en tant que contributeur.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtre les projets où l'utilisateur est soit créateur soit contributeur
        return Project.objects.filter(
            Q(creator=self.request.user)
            | Q(contributor_set__contributor=self.request.user)
        ).distinct().order_by('-created_time')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if not response.data['results']:
            response.data['message'] = (
                (
                    "Aucun projet trouvé. Créez-en un ou demandez à être ajouté "
                    "en tant que contributeur."
                )
            )
        return response


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, mettre à jour ou supprimer un projet.
    La suppression et la mise à jour sont réservées aux créateurs du projet.
    """
    queryset = Project.objects.all().prefetch_related('contributors')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_permissions(self):
        # Différencie les permissions pour les méthodes sécurisées et non sécurisées
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), IsContributor()]
        return [permissions.IsAuthenticated(), IsCreator()]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data['message'] = "Détails du projet récupérés avec succès."
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Projet mis à jour avec succès."
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Le projet a été supprimé avec succès."},
            status=status.HTTP_200_OK
        )


class IssueCreateView(generics.CreateAPIView):
    """
    Vue pour créer une issue dans un projet spécifique.
    Seuls les contributeurs peuvent créer des issues.
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_project(self):
        # Récupère le projet pour l'ID spécifié
        project = Project.objects.get(pk=self.kwargs['project_id'])
        # Vérifie si l'utilisateur est un contributeur du projet ou le créateur
        is_contributor = Contributor.objects.filter(
            project=project, contributor=self.request.user
        ).exists()
        if not is_contributor and project.creator != self.request.user:
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet.")
        return project

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project, creator=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Issue créée avec succès pour le projet."
        return response


class IssueListView(generics.ListAPIView):
    """
    Vue pour lister toutes les issues d'un projet spécifique.
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        # Filtre les issues par projet et les trie par date de création
        project = Project.objects.get(pk=self.kwargs['project_id'])
        return Issue.objects.filter(project=project).order_by('-created_time')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['message'] = "Liste des issues récupérée avec succès."
        return response


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, mettre à jour ou supprimer une issue spécifique.
    Seul le créateur peut modifier ou supprimer.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), IsContributor()]
        return [permissions.IsAuthenticated(), IsCreator()]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data['message'] = "Détails de l'issue récupérés avec succès."
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Issue mise à jour avec succès."
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "L'issue a été supprimée avec succès."},
            status=status.HTTP_200_OK
        )


class CommentCreateView(generics.CreateAPIView):
    """
    Vue pour créer un commentaire dans une issue spécifique. Seuls les contributeurs du
    projet parent peuvent ajouter des commentaires.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_issue(self):
        issue = Issue.objects.get(pk=self.kwargs['issue_id'])
        project = issue.project
        # Vérifie si l'utilisateur est contributeur ou créateur du projet
        if (
            not Contributor.objects.filter(
                project=project, contributor=self.request.user
            ).exists()
            and project.creator != self.request.user
        ):
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet.")
        return issue

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_id'])
        # Forcer l'évaluation de la permission
        self.check_object_permissions(self.request, issue)
        serializer.save(creator=self.request.user, issue=issue)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Commentaire ajouté avec succès à l'issue."
        return response


class CommentListView(generics.ListAPIView):
    """
    Vue pour lister tous les commentaires d'une issue spécifique.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        issue = Issue.objects.get(pk=self.kwargs['issue_id'])
        return Comment.objects.filter(issue=issue).order_by('-created_time')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['message'] = "Liste des commentaires récupérée avec succès."
        return response


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, mettre à jour ou supprimer un commentaire spécifique.
    Seul le créateur peut modifier ou supprimer un commentaire.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), IsContributor()]
        return [permissions.IsAuthenticated(), IsCreator()]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data['message'] = "Détails du commentaire récupérés avec succès."
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Commentaire mis à jour avec succès."
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Le commentaire a été supprimée avec succès."},
            status=status.HTTP_200_OK
        )
