from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    """
    Gestionnaire de modèle personnalisé pour le modèle User.
    Fournit des méthodes de création d'utilisateurs et de superutilisateurs.
    """
    def create_user(self, username, email, age, password=None, **extra_fields):
        """
        Crée et retourne un utilisateur avec un email, un nom d'utilisateur et un âge.
        """
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")
        if not username:
            raise ValueError("L'utilisateur doit avoir un nom d'utilisateur")
        if age < 15:
            raise ValueError("Vous devez avoir au moins 15 ans pour vous inscrire")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, age, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        """
        Crée et retourne un superutilisateur avec un email, un nom d'utilisateur
        et un âge.
        Le superutilisateur doit avoir les droits 'is_staff' et 'is_superuser'.
        """
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(username, email, age, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle utilisateur personnalisé avec des champs spécifiques pour la plateforme.
    Inclut des informations additionnelles comme la possibilité de contact
    et de partage de données.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Les relations uniques sont ajoutées pour la compatibilité avec le modèle
    # utilisateur personnalisé
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Nom unique pour éviter les conflits
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Nom unique pour éviter les conflits
        blank=True
    )

    # Le UserManager est assigné comme gestionnaire d'objets par défaut
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'age']

    def __str__(self):
        """Retourne une représentation lisible de l'utilisateur."""
        return self.username


class Contributor(models.Model):
    """
    Modèle représentant un contributeur à un projet.
    Chaque enregistrement relie un utilisateur à un projet spécifique.
    """
    contributor = models.ForeignKey(
        User, related_name="contributions", on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        'api.Project',
        related_name="contributor_set",
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Retourne le nom d'utilisateur du contributeur."""
        return self.contributor.username
