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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileUpdateView(generics.UpdateAPIView):
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
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Suppression de l'utilisateur : {user}")

        if user.is_authenticated:
            # Suppression en cascade de toutes les ressources associées
            Project.objects.filter(owner=user).delete()
            Contributor.objects.filter(user=user).delete()
            Issue.objects.filter(creator__user=user).delete()
            Comment.objects.filter(creator__user=user).delete()
            user.delete()

            logger.info("Compte et données associées supprimés avec succès.")
            return Response(
                {"message": "Compte et données associées supprimés avec succès."},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            logger.warning("Utilisateur non trouvé ou non authentifié.")
            return Response({"detail": "Utilisateur non trouvé", "code": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)


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
        return Response({"message": "Contributeur ajouté avec succès.", "data": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Inscription réussie !", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Vous êtes authentifié !"})
