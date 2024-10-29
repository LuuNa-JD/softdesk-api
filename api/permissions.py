import logging
from rest_framework import permissions
from api.models import Project


class IsContributor(permissions.BasePermission):
    """
    Permission permettant seulement aux contributeurs ou au propriétaire d'accéder à un projet et à ses composants.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            is_owner = obj.owner == request.user
            is_contributor = obj.contributors.filter(user=request.user).exists()
            return is_owner or is_contributor
        if hasattr(obj, 'project'):
            is_owner = obj.project.owner == request.user
            is_contributor = obj.project.contributors.filter(user=request.user).exists()
            return is_owner or is_contributor
        return False

class IsCreator(permissions.BasePermission):
    """
    Permission permettant seulement au créateur ou au propriétaire d'une ressource de la modifier ou de la supprimer.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Project):
            is_owner = obj.owner == request.user
            return is_owner

        # Ajout de logs pour vérifier la correspondance du créateur
        if hasattr(obj, 'creator'):
            is_creator = obj.creator == request.user or (hasattr(obj.creator, 'user') and obj.creator.user == request.user)
            return is_creator

        return False
