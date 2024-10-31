from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Si une exception `PermissionDenied` ou `NotAuthenticated` est interceptée
    if response is not None and response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            "message": (
                (
                    "Accès refusé : vous n'avez pas les permissions nécessaires "
                    "pour effectuer cette action."
                )
            )
        }
    # Personnalisation du message pour un 401 Unauthorized
    elif response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {
            "message": (
                "Authentification requise : veuillez fournir vos "
                "informations d'identification."
            )
        }

    elif response is not None and response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            "message": "La ressource demandée est introuvable."
        }

    return response
