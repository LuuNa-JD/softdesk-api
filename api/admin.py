from django.contrib import admin
from .models import Project, Issue, Comment
from users.models import Contributor


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les projets.
    """
    list_display = ('title', 'creator', 'type', 'created_time')
    list_filter = ('type', 'created_time')
    search_fields = ('title', 'description', 'creator__username')
    ordering = ('-created_time',)

    def get_contributors(self, obj):
        contributors = [
            contributor.contributor.username
            for contributor in obj.contributors.all()
        ]
        return ", ".join(contributors)
    get_contributors.short_description = "Contributeurs"


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les issues.
    """
    list_display = (
        'title', 'project', 'creator', 'assignee', 'priority', 'status', 'created_time'
    )
    list_filter = ('priority', 'status', 'created_time', 'project')
    search_fields = (
        'title', 'description', 'creator__username',
        'assignee__username', 'project__title'
    )
    ordering = ('-created_time',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les commentaires.
    """
    list_display = ('content', 'creator', 'issue', 'created_time')
    list_filter = ('created_time', 'issue')
    search_fields = ('content', 'creator__username', 'issue__title')
    ordering = ('-created_time',)
