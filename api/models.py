from django.db import models
from users.models import User
from users.models import Contributor
import uuid


class Project(models.Model):
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

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    owner = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)  # Horodatage

    def __str__(self):
        return self.title


class Issue(models.Model):
    PRIORITY_LOW = 'LOW'
    PRIORITY_MEDIUM = 'MEDIUM'
    PRIORITY_HIGH = 'HIGH'

    PRIORITIES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    TAG_BUG = 'BUG'
    TAG_FEATURE = 'FEATURE'
    TAG_TASK = 'TASK'

    TAGS = [
        (TAG_BUG, 'Bug'),
        (TAG_FEATURE, 'Feature'),
        (TAG_TASK, 'Task'),
    ]

    STATUS_TODO = 'To Do'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_FINISHED = 'Finished'

    STATUSES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_FINISHED, 'Finished'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name="issues", on_delete=models.CASCADE)
    creator = models.ForeignKey(Contributor, related_name="created_issues", on_delete=models.CASCADE)
    assignee = models.ForeignKey(Contributor, related_name="assigned_issues", on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=6, choices=PRIORITIES, default=PRIORITY_LOW)
    tag = models.CharField(max_length=7, choices=TAGS, default=TAG_TASK)
    status = models.CharField(max_length=12, choices=STATUSES, default=STATUS_TODO)
    created_time = models.DateTimeField(auto_now_add=True)  # Horodatage

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID unique
    content = models.TextField()
    issue = models.ForeignKey(Issue, related_name="comments", on_delete=models.CASCADE)
    creator = models.ForeignKey(Contributor, related_name="comments", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)  # Horodatage

    def __str__(self):
        return f"Comment by {self.creator.user.username} on {self.issue.title}"
