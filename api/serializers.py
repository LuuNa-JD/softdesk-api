from rest_framework import serializers
from .models import Project, Issue, Comment
from users.models import Contributor


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
    assigne_a = serializers.CharField(allow_blank=True, required=False)
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
                  'priority', 'tag', 'status', 'created_time', 'assigne_a']

    def get_creator(self, instance):
        return instance.creator.username

    def get_created_time(self, obj):
        return obj.created_time.strftime('%d %B %Y, %H:%M')


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
