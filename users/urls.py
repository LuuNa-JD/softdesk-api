from django.urls import path
from .views import (
    register_user,
    protected_view,
    UserDetailView,
    UserProfileUpdateView,
    UserDeleteView,
    AddContributorView
)

urlpatterns = [
    # Enregistrement d'un utilisateur
    path('register/', register_user, name='register_user'),

    # Vue protégée
    path('protected/', protected_view, name='protected_view'),

    # Gestion du profil utilisateur
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', UserDeleteView.as_view(), name='profile-delete'),

    # Gestion des contributeurs d'un projet
    path(
        'projects/<int:project_id>/add_contributor/',
        AddContributorView.as_view(),
        name='add-contributor'
    ),
]
