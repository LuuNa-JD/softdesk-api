from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project, Issue, Comment


User = get_user_model()


class ProjectTests(TestCase):
    def setUp(self):
        # Crée un client API et des utilisateurs de test
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user1', email='user1@example.com', age=25, password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', age=25, password='pass123'
        )
        self.client.force_authenticate(user=self.user)

        # Crée un projet de test
        self.project = Project.objects.create(
            title="Test Project",
            description="Description",
            type="back-end",
            creator=self.user
        )

    def test_create_project(self):
        # Teste la création d'un projet via l'API
        data = {
            "title": "New Project",
            "description": "New Description",
            "type": "front-end"
        }
        response = self.client.post("/api/projects/create/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'],
            (
                "Projet créé avec succès ! "
                "Vous êtes ajouté comme propriétaire et contributeur."
            )
        )

    def test_project_list(self):
        # Teste la récupération de la liste des projets
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Project", str(response.data))

    def test_project_detail_permissions(self):
        # Teste que seul le créateur ou un contributeur peut voir les détails
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/projects/{self.project.id}/")
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )  # Permission refusée pour user2


class IssueTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user1', email='user1@example.com', age=25, password='pass123'
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Description",
            type="back-end",
            creator=self.user
        )
        self.client.force_authenticate(user=self.user)

        # Crée une issue de test
        self.issue = Issue.objects.create(
            title="Test Issue",
            description="Issue description",
            project=self.project,
            creator=self.user
        )

    def test_create_issue(self):
        # Teste la création d'une issue
        data = {
            "title": "New Issue",
            "description": "Issue description",
            "priority": "HIGH",
            "tag": "BUG",
            "status": "To Do"
        }
        response = self.client.post(
            f"/api/projects/{self.project.id}/issues/create/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'],
            "Issue créée avec succès pour le projet."
        )

    def test_issue_list(self):
        # Teste la récupération des issues pour un projet
        response = self.client.get(f"/api/projects/{self.project.id}/issues/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Issue", str(response.data))


class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user1', email='user1@example.com', age=25, password='pass123'
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Description",
            type="back-end",
            creator=self.user
        )
        self.issue = Issue.objects.create(
            title="Test Issue",
            description="Issue description",
            project=self.project,
            creator=self.user
        )
        self.client.force_authenticate(user=self.user)

        # Crée un commentaire de test
        self.comment = Comment.objects.create(
            content="Test comment",
            issue=self.issue,
            creator=self.user
        )

    def test_create_comment(self):
        # Teste la création d'un commentaire pour une issue
        data = {"content": "New comment"}
        response = self.client.post(
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/comments/create/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'],
            "Commentaire ajouté avec succès à l'issue."
        )

    def test_comment_list(self):
        # Teste la récupération des commentaires pour une issue
        response = self.client.get(
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/comments/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test comment", str(response.data))
