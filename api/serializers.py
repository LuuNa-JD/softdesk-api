from rest_framework import serializers
from .models import Project, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.id')
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    issue = serializers.ReadOnlyField(source='issue.id')
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Comment
        fields = '__all__'
