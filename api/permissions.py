from rest_framework import permissions
from users.models import Contributor
from api.models import Project, Issue, Comment


class IsContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'objet est une instance de Project, Issue ou Comment
        if isinstance(obj, Project):
            project = obj
        elif isinstance(obj, Issue):
            project = obj.project
        elif isinstance(obj, Comment):
            project = obj.issue.project
        else:
            return False

        # Vérifie si l'utilisateur est un contributeur du projet
        return Contributor.objects.filter(project=project, contributor=request.user).exists() or project.creator == request.user


class IsCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
