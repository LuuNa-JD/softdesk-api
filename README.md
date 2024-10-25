
# SoftDesk API

SoftDesk est une API RESTful pour la gestion de projets, d'issues, et de commentaires.

## Prérequis

- Python 3.10+
- Django 4.x
- Django REST Framework
- Poetry (pour la gestion des dépendances)

## Installation

### 1. Cloner ce dépôt

Clonez ce dépôt en local en utilisant la commande suivante :

```bash
git clone https://github.com/LuuNa-JD/softdesk-api.git
cd softdesk_api
```

### 3. Installer les dépendances

Installez les dépendances nécessaires avec Poetry :

```bash
poetry install
```

### 4. Appliquer les migrations de base de données

Exécutez les migrations pour préparer la base de données :

```bash
poetry run python manage.py migrate
```

## Lancement

Pour démarrer l'API en local, exécutez la commande suivante :

```bash
poetry run python manage.py runserver
```

## Fonctionnalités

- Gestion des utilisateurs et des contributeurs
- Création de projets, d'issues, et de commentaires
- Authentification via Json Web Token (JWT)

## Tests

Vous pouvez utiliser l’outil **Postman** ou **curl** pour tester les différents points de terminaison de l’API.
