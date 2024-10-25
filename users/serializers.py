from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User
from users.models import Contributor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_age(self, value):
        """Vérifie que l'utilisateur a au moins 15 ans"""
        if value and value < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
        return value

    def create(self, validated_data):
        """Création d'un utilisateur avec un mot de passe hashé"""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            age=validated_data['age'],
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Mot de passe optionnel
    username = serializers.CharField(required=False)  # Nom d'utilisateur optionnel

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'password', 'can_be_contacted', 'can_data_be_shared']

    def update(self, instance, validated_data):
        # Met à jour le mot de passe si fourni
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Authentifier avec `username` au lieu de `email`
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Aucun compte actif trouvé avec ces identifiants.")

        # Appelle la méthode de validation du Serializer parent pour générer le token
        data = super().validate(attrs)
        return data

class AddContributorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        model = Contributor
        fields = ['username', 'role']

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Cet utilisateur n'existe pas.")
        return user

    def create(self, validated_data):
        project = self.context['project']
        user = validated_data['username']
        contributor, created = Contributor.objects.get_or_create(user=user, project=project)
        return contributor
