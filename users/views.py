from rest_framework import viewsets, permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserUpdateSerializer,
    UserSerializer,
    ContributorSerializer
)
from .models import User
from api.permissions import IsCreator
from api.models import Project, Contributor, Issue, Comment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    Vue pour la gestion des utilisateurs, avec pagination et
    permissions d'authentification.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue pour obtenir un token JWT en utilisant un serializer personnalisé.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Vue pour mettre à jour les informations du profil utilisateur.
    Seul l'utilisateur connecté peut accéder et modifier son propre profil.
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Profil mis à jour avec succès."
        return response


class UserDeleteView(APIView):
    """
    Vue pour supprimer un utilisateur et toutes ses ressources associées
    (projets, contributeurs, issues, commentaires).
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            # Journalisation avant suppression
            logger.info(
                f"Suppression de l'utilisateur {user.username} "
                f"et de toutes les ressources associées."
            )

            # Suppression en cascade de toutes les ressources associées
            Project.objects.filter(creator=user).delete()
            Contributor.objects.filter(contributor=user).delete()
            Issue.objects.filter(creator=user).delete()
            Comment.objects.filter(creator=user).delete()
            user.delete()

            logger.info(f"Utilisateur {user.username} supprimé avec succès.")
            return Response(
                {"message": "L'utilisateur a été supprimé avec succès."},
                status=status.HTTP_200_OK
            )

        # Journalisation en cas d'échec
        logger.warning("Tentative de suppression d'un utilisateur non authentifié.")
        return Response(
            {"detail": "Utilisateur non trouvé", "code": "user_not_found"},
            status=status.HTTP_404_NOT_FOUND
        )


class AddContributorView(generics.CreateAPIView):
    """
    Vue pour ajouter un utilisateur en tant que contributeur à un projet.
    Seul le créateur du projet peut ajouter des contributeurs.
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreator]

    def get_project(self):
        # Récupère le projet en utilisant l'ID de l'URL
        try:
            return Project.objects.get(pk=self.kwargs['project_id'])
        except Project.DoesNotExist:
            logger.error("Projet non trouvé.")
            return None

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)

    def post(self, request, *args, **kwargs):
        project = self.get_project()
        if project is None:
            return Response(
                {"detail": "Projet non trouvé."},
                status=status.HTTP_404_NOT_FOUND
            )

        if project.creator != request.user:
            logger.warning(
                f"Tentative d'ajout de contributeur par un utilisateur non créateur : "
                f"{request.user.username}"
            )
            return Response(
                {"detail": "Seul le créateur peut ajouter des contributeurs."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            data=request.data,
            context={'project': project}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Contributeur ajouté avec succès.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Vue pour inscrire un nouvel utilisateur.
    Accessible sans authentification.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Nouvel utilisateur inscrit : {serializer.data['username']}")
        return Response(
            {"message": "Inscription réussie !", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    logger.warning("Échec de l'inscription en raison de données invalides.")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Vue protégée nécessitant une authentification.
    Retourne un message de confirmation.
    """
    return Response({"message": "Vous êtes authentifié !"})
