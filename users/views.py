from rest_framework import viewsets, permissions, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserUpdateSerializer
from .models import User
from .serializers import UserSerializer, AddContributorSerializer
from api.permissions import IsContributor
from api.models import Project
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import logging


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer  # Utilise le serializer de mise à jour
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


logger = logging.getLogger(__name__)


class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Utilisateur authentifié : {user}")
        logger.info(f"Est authentifié : {user.is_authenticated}")

        if user.is_authenticated:
            user.delete()
            logger.info("Compte supprimé avec succès.")
            return Response({"message": "Compte supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
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

        # Passe le contexte avec le projet dans le serializer
        serializer = self.get_serializer(data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])  # Permet l'accès à tous
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
