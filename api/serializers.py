from rest_framework import serializers
from .models import Project, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    title = serializers.CharField(
        error_messages={
            'blank': "Le titre du projet ne peut pas être vide.",
            'max_length': "Le titre est trop long. Limitez à 255 caractères."
        }
    )

    class Meta:
        model = Project
        fields = '__all__'  # Inclut tous les champs du modèle

    def get_created_time(self, obj):
        return obj.created_time.strftime('%d %B %Y, %H:%M')


class IssueSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    project = serializers.ReadOnlyField(source='project.id')
    creator_name = serializers.ReadOnlyField(source='creator.user.username')
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
                  'priority', 'tag', 'status', 'created_time']

    def get_created_time(self, obj):
        return obj.created_time.strftime('%d %B %Y, %H:%M')


class CommentSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    issue = serializers.ReadOnlyField(source='issue.id')
    creator_name = serializers.ReadOnlyField(source='creator.user.username')
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
