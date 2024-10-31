from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User
from users.models import Contributor


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'utilisateurs. Inclut la gestion des mots de passe
    et la validation de l'âge minimum requis.
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'age', 'can_be_contacted',
            'can_data_be_shared', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }  # Rend le champ `password` en écriture seule

    def validate_age(self, value):
        """Vérifie que l'utilisateur a au moins 15 ans"""
        if value and value < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour vous inscrire."
            )
        return value

    def validate_email(self, value):
        """Vérifie que l'adresse email est unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Un utilisateur avec cet email existe déjà."
            )
        return value

    def validate_username(self, value):
        """Vérifie que le nom d'utilisateur est unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Ce nom d'utilisateur est déjà pris."
            )
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
    """
    Serializer pour la mise à jour des informations utilisateur.
    Permet de changer le mot de passe, le nom d'utilisateur,
    et autres champs optionnels.
    """
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'age', 'password',
            'can_be_contacted', 'can_data_be_shared'
        ]

    def validate_email(self, value):
        """Vérifie que l'adresse email est unique lors de la mise à jour."""
        user_id = self.instance.id
        if User.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError(
                "Un utilisateur avec cet email existe déjà."
            )
        return value

    def validate_username(self, value):
        """Vérifie que le nom d'utilisateur est unique lors de la mise à jour."""
        user_id = self.instance.id
        if User.objects.exclude(id=user_id).filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return value

    def update(self, instance, validated_data):
        """
        Met à jour les informations de l'utilisateur, y compris le mot de passe
        s'il est fourni.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer pour l'obtention de jetons JWT basé sur le nom d'utilisateur.
    """
    username = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Authentifier avec `username` au lieu de `email`
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                "Aucun compte actif trouvé avec ces identifiants."
            )

        # Génère le jeton JWT en appelant la méthode de validation parent
        data = super().validate(attrs)
        return data


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour ajouter un utilisateur en tant que contributeur à un projet.
    Prend le `username` en entrée et lie le contributeur au projet spécifié
    dans le contexte.
    """
    contributor_username = serializers.CharField(
        write_only=True,
        help_text="Nom d'utilisateur du contributeur à ajouter."
    )

    contributor_added = serializers.CharField(
        source='contributor.username',
        read_only=True,
        help_text="Nom d'utilisateur du contributeur ajouté et affiché."
    )

    class Meta:
        model = Contributor
        fields = ['id', 'contributor_username', 'contributor_added', 'project']
        extra_kwargs = {'project': {'required': False}}

    def create(self, validated_data):
        """
        Crée un contributeur pour un projet donné en fonction du `username` fourni.
        """
        project = self.context['project']
        username = validated_data.pop('contributor_username')
        try:
            contributor = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"contributor_username": "Utilisateur non trouvé."}
            )
        return Contributor.objects.create(project=project, contributor=contributor)
