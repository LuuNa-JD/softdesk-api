from rest_framework import serializers
from .models import Project, Issue, Comment
from users.models import Contributor
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()
    title = serializers.CharField(
        error_messages={
            'blank': "Le titre du projet ne peut pas être vide.",
            'max_length': "Le titre est trop long. Limitez à 255 caractères."
        }
    )

    class Meta:
        model = Project
        fields = '__all__'

    def get_creator(self, instance):
        return instance.creator.username

    def get_contributors(self, instance):
        contributors = Contributor.objects.filter(project=instance)
        return [contributor.contributor.username for contributor in contributors]

    def get_created_time(self, obj):
        return obj.created_time.strftime('%d %B %Y, %H:%M')


class IssueSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    project = serializers.ReadOnlyField(source='project.id')
    assignee = serializers.CharField(write_only=True, required=False)  # Accepte un username en entrée
    assignee_username = serializers.ReadOnlyField(source='assignee.username')  # Affiche le username en sortie
    creator_name = serializers.StringRelatedField(source='creator.username', read_only=True)
    title = serializers.CharField(
        error_messages={
            'blank': "Le titre de l'issue ne peut pas être vide.",
        }
    )
    description = serializers.CharField(
        error_messages={
            'blank': "La description de l'issue ne peut pas être vide.",
        }
    )

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'creator_name',
                  'priority', 'tag', 'status', 'created_time', 'assignee', 'assignee_username']

    def get_creator(self, instance):
        return instance.creator.username

    def get_created_time(self, obj):
        return obj.created_time.strftime('%d %B %Y, %H:%M')

    def validate_assignee(self, value):
        try:
            user = User.objects.get(username=value)  # Recherche par username
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur avec ce username n'existe pas.")

    def create(self, validated_data):
        assignee_username = validated_data.pop('assignee', None)
        if assignee_username:
            validated_data['assignee'] = self.validate_assignee(assignee_username)

        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assignee_username = validated_data.pop('assignee', None)
        if assignee_username:
            validated_data['assignee'] = self.validate_assignee(assignee_username)

        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    issue = serializers.ReadOnlyField(source='issue.id')
    creator_name = serializers.StringRelatedField()
    content = serializers.CharField(
        error_messages={
            'blank': "Le contenu du commentaire ne peut pas être vide.",
        }
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'issue', 'creator_name', 'created_time']

    def get_created_time(self, obj):
        return obj.created_time.strftime('%d %B %Y, %H:%M')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['creator'] = request.user
        return super().create(validated_data)
