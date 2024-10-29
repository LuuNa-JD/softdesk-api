from rest_framework import viewsets, permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserUpdateSerializer, UserSerializer, AddContributorSerializer
from .models import User
from api.permissions import IsContributor
from api.models import Project, Contributor, Issue, Comment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination  # Pagination pour les listes d'utilisateurs
    permission_classes = [permissions.IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Utilisateur authentifié : {user}")

        if user.is_authenticated:
            # Supprimer les projets créés par l'utilisateur
            Project.objects.filter(owner=user).delete()

            # Supprimer toutes les contributions de l'utilisateur
            Contributor.objects.filter(user=user).delete()

            # Supprimer les issues créées par l'utilisateur
            Issue.objects.filter(creator__user=user).delete()

            # Supprimer les commentaires créés par l'utilisateur
            Comment.objects.filter(creator__user=user).delete()

            # Supprimer l'utilisateur lui-même
            user.delete()

            logger.info("Compte et données associées supprimés avec succès.")
            return Response({"message": "Compte et données associées supprimés avec succès."}, status=status.HTTP_204_NO_CONTENT)
        else:
            logger.warning("Utilisateur non trouvé ou non authentifié.")
            return Response({"detail": "User not found", "code": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)


class AddContributorView(generics.CreateAPIView):
    serializer_class = AddContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_project(self):
        return Project.objects.get(pk=self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)

    def post(self, request, *args, **kwargs):
        project = self.get_project()
        if project is None:
            return Response({"detail": "Projet non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        if project.owner != request.user:
            return Response({"detail": "Seul le propriétaire peut ajouter des contributeurs."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Vous êtes authentifié !"})
