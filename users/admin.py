from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Contributor


class UserAdmin(BaseUserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle User personnalisé.
    """
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {
            'fields': ('age', 'can_be_contacted', 'can_data_be_shared')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'age', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'age', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)


# Enregistre le modèle User avec la configuration personnalisée UserAdmin
admin.site.register(User, UserAdmin)


class ContributorAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Contributor.
    """
    list_display = ('contributor', 'project')
    list_filter = ('project',)
    search_fields = ('contributor__username', 'project__title')
    ordering = ('project',)


# Enregistre le modèle Contributor avec ContributorAdmin
admin.site.register(Contributor, ContributorAdmin)
