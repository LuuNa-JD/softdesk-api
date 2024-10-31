from rest_framework import permissions
from users.models import Contributor
from api.models import Project, Issue, Comment


class IsContributor(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est contributeur
    ou créateur d'un projet.
    """

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur a accès à l'objet (Project, Issue ou Comment).
        Retourne True si l'utilisateur est contributeur ou créateur du projet associé.
        """

        # Détermine le projet associé en fonction de l'objet reçu
        if isinstance(obj, Project):
            project = obj
        elif isinstance(obj, Issue):
            project = obj.project
        elif isinstance(obj, Comment):
            project = obj.issue.project
        else:
            return False  # Retourne False si l'objet n'est pas associé à un projet

        # Vérifie si l'utilisateur est un contributeur du projet
        is_contributor = Contributor.objects.filter(project=project, contributor=request.user).exists()
        # Vérifie si l'utilisateur est le créateur du projet
        is_creator = project.creator == request.user

        # Retourne True si l'utilisateur est soit contributeur soit créateur
        return is_contributor or is_creator


class IsCreator(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est le créateur de l'objet.
    Applicable aux objets ayant un attribut 'creator'.
    """

    def has_object_permission(self, request, view, obj):
        """
        Retourne True si l'utilisateur est le créateur de l'objet.
        """
        return obj.creator == request.user
