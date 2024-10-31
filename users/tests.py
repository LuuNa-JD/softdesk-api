from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Contributor
from api.models import Project

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        # Configuration initiale avec un client API et des utilisateurs de test
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user1', email='user1@example.com', age=25, password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', age=30, password='password123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            title="Test Project",
            description="Project description",
            type="back-end",
            creator=self.user
        )

    def test_create_user(self):
        """Test de création d'un nouvel utilisateur."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "age": 20,
            "password": "newpassword"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["data"]["username"], "newuser")

    def test_update_user_profile(self):
        """Test de mise à jour du profil utilisateur."""
        data = {"email": "updateduser@example.com", "age": 26}
        response = self.client.put("/api/profile/update/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updateduser@example.com")
        self.assertEqual(response.data["message"], "Profil mis à jour avec succès.")

    def test_delete_user(self):
        """
        Test de suppression d'un utilisateur et de toutes ses ressources associées.
        """
        user_id = self.user.id

        # Supprime l'utilisateur
        response = self.client.delete("/api/profile/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Vérifie que l'utilisateur et les projets associés sont bien supprimés
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(Project.objects.filter(creator_id=user_id).exists())

    def test_add_contributor(self):
        """Test de l'ajout d'un contributeur par le créateur du projet."""
        data = {"contributor_username": "user2"}
        response = self.client.post(
            f"/api/projects/{self.project.id}/add_contributor/", data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Contributeur ajouté avec succès.")
        self.assertTrue(
            Contributor.objects.filter(
                contributor=self.user2, project=self.project
            ).exists()
        )

    def test_non_creator_cannot_add_contributor(self):
        """
        Vérifie qu'un utilisateur non créateur ne peut pas ajouter de contributeur.
        """
        self.client.force_authenticate(user=self.user2)
        data = {"contributor_username": "user1"}
        response = self.client.post(
            f"/api/projects/{self.project.id}/add_contributor/", data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
