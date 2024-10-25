"""
URL configuration for softdesk_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from users.views import CustomTokenObtainPairView
from users.views import protected_view
from users.views import register_user, UserProfileUpdateView, UserDeleteView
from users.views import AddContributorView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', register_user, name='register_user'),
    path('api/protected/', protected_view, name='protected_view'),
    path('api/profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('api/profile/delete/', UserDeleteView.as_view(), name='profile-delete'),
    path('api/projects/<int:project_id>/add_contributor/', AddContributorView.as_view(), name='add-contributor'),
    path('api/', include('users.urls')),
    path('api/', include('api.urls')),
]
