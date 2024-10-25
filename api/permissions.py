from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsProjectContributorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.contributors.filter(id=request.user.id).exists() or obj.author_user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_user == request.user


class IsContributor(permissions.BasePermission):
    """
    Permission permettant seulement aux contributeurs d'accéder à un projet et à ses composants.
    """

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'objet est un projet et si l'utilisateur est un contributeur
        if hasattr(obj, 'contributors'):
            return obj.contributors.filter(user=request.user).exists()

        # Vérifie si l'objet est une issue ou un commentaire et si l'utilisateur est contributeur du projet parent
        if hasattr(obj, 'project'):
            return obj.project.contributors.filter(user=request.user).exists()

        return False

class IsCreator(permissions.BasePermission):
    """
    Permission permettant seulement au créateur d'une ressource de la modifier ou de la supprimer.
    """

    def has_object_permission(self, request, view, obj):
        # Lecture seule autorisée pour les contributeurs (si `IsContributor` est appliqué)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Autorisation de modification/suppression seulement pour le créateur
        return obj.creator == request.user.contributions.get(project=obj.project)
