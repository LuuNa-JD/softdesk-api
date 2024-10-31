from django.db import models
from users.models import User, Contributor
import uuid


class Project(models.Model):
    # Types de projets
    BACKEND = 'back-end'
    FRONTEND = 'front-end'
    IOS = 'iOS'
    ANDROID = 'android'

    PROJECT_TYPES = [
        (BACKEND, 'Back-end'),
        (FRONTEND, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]

    title = models.CharField(max_length=255, help_text="Titre du projet")
    description = models.TextField(help_text="Description détaillée du projet")
    type = models.CharField(max_length=50, choices=PROJECT_TYPES, help_text="Type de projet (front-end, back-end, etc.)")
    creator = models.ForeignKey(User, related_name="projects_created", on_delete=models.CASCADE, help_text="Créateur du projet")
    contributors = models.ManyToManyField(Contributor, related_name="projects_contributed", blank=True, help_text="Contributeurs associés au projet")
    created_time = models.DateTimeField(auto_now_add=True, help_text="Date de création du projet")  # Horodatage

    def __str__(self):
        return self.title  # Retourne le titre comme représentation du projet


class Issue(models.Model):
    # Priorités de l'issue
    PRIORITY_LOW = 'LOW'
    PRIORITY_MEDIUM = 'MEDIUM'
    PRIORITY_HIGH = 'HIGH'

    PRIORITIES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    # Tags de l'issue
    TAG_BUG = 'BUG'
    TAG_FEATURE = 'FEATURE'
    TAG_TASK = 'TASK'

    TAGS = [
        (TAG_BUG, 'Bug'),
        (TAG_FEATURE, 'Feature'),
        (TAG_TASK, 'Task'),
    ]

    # Statuts de l'issue
    STATUS_TODO = 'To Do'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_FINISHED = 'Finished'

    STATUSES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_FINISHED, 'Finished'),
    ]

    title = models.CharField(max_length=100, help_text="Titre de l'issue")
    description = models.TextField(help_text="Description détaillée de l'issue")
    project = models.ForeignKey(Project, related_name="issues", on_delete=models.CASCADE, help_text="Projet associé à cette issue")
    creator = models.ForeignKey(User, related_name="created_issues", on_delete=models.CASCADE, help_text="Utilisateur qui a créé l'issue")
    assignee = models.ForeignKey(User, related_name="assigned_issues", on_delete=models.CASCADE, null=True, blank=True, help_text="Utilisateur assigné à cette issue")
    priority = models.CharField(max_length=6, choices=PRIORITIES, default=PRIORITY_LOW, help_text="Priorité de l'issue")
    tag = models.CharField(max_length=7, choices=TAGS, default=TAG_TASK, help_text="Tag de l'issue")
    status = models.CharField(max_length=12, choices=STATUSES, default=STATUS_TODO, help_text="Statut de l'issue")
    created_time = models.DateTimeField(auto_now_add=True, help_text="Date de création de l'issue")

    def __str__(self):
        return self.title  # Retourne le titre comme représentation de l'issue


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Identifiant unique du commentaire")
    content = models.TextField(help_text="Contenu du commentaire")
    issue = models.ForeignKey(Issue, related_name="comments", on_delete=models.CASCADE, help_text="Issue associée au commentaire")
    creator = models.ForeignKey(User, related_name="created_comments", on_delete=models.CASCADE, help_text="Utilisateur ayant créé le commentaire")
    created_time = models.DateTimeField(auto_now_add=True, help_text="Date de création du commentaire")

    def __str__(self):
        # Affiche une description lisible du commentaire
        return f"Comment by {self.creator.user.username} on {self.issue.title}"
