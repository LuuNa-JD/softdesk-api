from rest_framework import serializers
from .models import Project, Issue, Comment
from users.models import Contributor
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Project, incluant le créateur,
    les contributeurs et un format personnalisé pour la date de création.
    """
    created_time = serializers.SerializerMethodField(help_text="Date de création formatée")
    creator = serializers.SerializerMethodField(help_text="Username du créateur du projet")
    contributors = serializers.SerializerMethodField(help_text="Liste des usernames des contributeurs")
    title = serializers.CharField(
        error_messages={
            'blank': "Le titre du projet ne peut pas être vide.",
            'max_length': "Le titre est trop long. Limitez à 255 caractères."
        },
        help_text="Titre du projet"
    )

    class Meta:
        model = Project
        fields = '__all__'

    def get_creator(self, instance):
        """Retourne le username du créateur du projet."""
        return instance.creator.username

    def get_contributors(self, instance):
        """Retourne une liste des usernames des contributeurs associés au projet."""
        contributors = Contributor.objects.filter(project=instance)
        return [contributor.contributor.username for contributor in contributors]

    def get_created_time(self, obj):
        """Formate la date de création au format jour/mois/année heure:minute."""
        return obj.created_time.strftime('%d %B %Y, %H:%M')


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Issue, incluant des champs pour l'assignee et le créateur.
    Permet de spécifier l'assignee par son username.
    """
    created_time = serializers.SerializerMethodField(help_text="Date de création formatée")
    project = serializers.ReadOnlyField(source='project.id', help_text="ID du projet associé")
    assignee = serializers.CharField(write_only=True, required=False, help_text="Username de l'utilisateur assigné")
    assignee_username = serializers.ReadOnlyField(source='assignee.username', help_text="Username de l'assignee")
    creator_name = serializers.StringRelatedField(source='creator.username', read_only=True, help_text="Nom d'utilisateur du créateur de l'issue")
    title = serializers.CharField(
        error_messages={
            'blank': "Le titre de l'issue ne peut pas être vide.",
            'max_length': "Le titre est trop long. Limitez à 100 caractères."
        },
        help_text="Titre de l'issue"
    )
    description = serializers.CharField(
        error_messages={
            'blank': "La description de l'issue ne peut pas être vide.",
        },
        help_text="Description détaillée de l'issue"
    )

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'creator_name',
                  'priority', 'tag', 'status', 'created_time', 'assignee', 'assignee_username']

    def get_creator(self, instance):
        return instance.creator.username

    def get_created_time(self, obj):
        """Formate la date de création au format jour/mois/année heure:minute."""
        return obj.created_time.strftime('%d %B %Y, %H:%M')

    def validate_assignee(self, value):
        """Vérifie que l'assignee existe bien en base de données."""
        try:
            user = User.objects.get(username=value)  # Recherche par username
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur avec ce username n'existe pas.")

    def create(self, validated_data):
        """Crée une issue en assignant le créateur actuel et en validant l'assignee."""
        assignee_username = validated_data.pop('assignee', None)
        if assignee_username:
            validated_data['assignee'] = self.validate_assignee(assignee_username)

        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Met à jour l'issue et assigne l'assignee si spécifié."""
        assignee_username = validated_data.pop('assignee', None)
        if assignee_username:
            validated_data['assignee'] = self.validate_assignee(assignee_username)

        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Comment, incluant le créateur et la date de création formatée.
    """
    created_time = serializers.SerializerMethodField(help_text="Date de création formatée")
    issue = serializers.ReadOnlyField(source='issue.id', help_text="ID de l'issue associée")
    creator_name = serializers.StringRelatedField(help_text="Nom d'utilisateur du créateur du commentaire")
    content = serializers.CharField(
        error_messages={
            'blank': "Le contenu du commentaire ne peut pas être vide.",
        },
        help_text="Contenu du commentaire"
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'issue', 'creator_name', 'created_time']

    def get_created_time(self, obj):
        """Formate la date de création au format jour/mois/année heure:minute."""
        return obj.created_time.strftime('%d %B %Y, %H:%M')

    def create(self, validated_data):
        """Crée un commentaire en assignant automatiquement l'utilisateur actuel comme créateur."""
        request = self.context.get('request')
        validated_data['creator'] = request.user
        return super().create(validated_data)
