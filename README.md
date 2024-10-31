
# SoftDesk API

## Table des matières

- [À propos du projet](#à-propos-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation et Démarrage](#installation-et-démarrage)
  - [1. Cloner ce dépôt](#1-cloner-ce-dépôt)
  - [2. Installer les dépendances](#2-installer-les-dépendances)
  - [3. Configurer la base de données](#3-configurer-la-base-de-données)
  - [4. Appliquer les migrations de base de données](#4-appliquer-les-migrations-de-base-de-données)
  - [5. Créer un superutilisateur](#5-créer-un-superutilisateur)
  - [6. Lancement](#6-lancement)
- [Authentification](#authentification)
- [Pagination](#pagination)
- [Test unitaires](#test-unitaires)
- [Code Linting et Conformité (Flake8)](#code-linting-et-conformité-flake8)
- [Technologies Utilisées](#technologies-utilisées)
- [Documentation API via Postman](#documentation-api-via-postman)
- [Auteur](#auteur)

## À propos du projet

SoftDesk API est une API RESTful développée pour faciliter la gestion des projets collaboratifs. Elle permet d’organiser les contributeurs autour de projets, de suivre les issues et les commentaires associés, avec une gestion des permissions et un accès sécurisé.

## Fonctionnalités

- **Gestion des utilisateurs** : Inscription, authentification JWT, gestion de profil, et permissions avancées.
- **Gestion des projets** : Création, consultation, mise à jour et suppression des projets avec des contributeurs associés.
- **Suivi des issues** : Création, mise à jour, et suivi des issues par projet, avec assignation à des utilisateurs.
- **Commentaires** : Ajout de commentaires aux issues, avec gestion d’auteurs et d’édition.
- **Sécurité et optimisation** : Permissions personnalisées, requêtes optimisées et pagination pour une efficacité maximale.

## Prérequis

- **Python** : Version 3.10 ou supérieure
- **Django** : Version 4.x
- **Django REST Framework**
- **Poetry** : Pour la gestion des dépendances

## Installation et Démarrage

### 1. Cloner ce dépôt

Clonez ce dépôt en local :

```bash
git clone https://github.com/LuuNa-JD/softdesk-api.git
cd softdesk_api
```

### 2. Installer les dépendances

Installez les dépendances nécessaires avec Poetry :

```bash
poetry install
```
### 3. Configurer la base de données

Par défaut, l’API utilise SQLite. Pour PostgreSQL, configurez les informations dans settings.py sous la section DATABASES.

### 4. Appliquer les migrations de base de données

Exécutez les migrations pour préparer la base de données :

```bash
poetry run python manage.py migrate
```

### 5. Créer un superutilisateur

Créez un superutilisateur pour accéder à l’interface d’administration :

```bash
poetry run python manage.py createsuperuser
```

### 6. Lancement

Pour démarrer l'API en local, exécutez la commande suivante :

```bash
poetry run python manage.py runserver
```
L'API sera accessible par défaut sur http://127.0.0.1:8000/.

## Authentification

L'API utilise JWT pour l'authentification. Pour obtenir un token, envoyez une requête POST à l'URL /api/token/ avec les identifiants d'un utilisateur enregistré. Le token sera renvoyé dans la réponse.

## Pagination

Les endpoints de liste utilisent une pagination par défaut de 10 éléments par page. Pour ajuster le nombre d’éléments retournés par page :

**Paramètres** :
- `page` : numéro de page.
- `page_size` : nombre d'éléments par page.

## Test unitaires

Pour exécuter les tests unitaires, utilisez la commande suivante :

```bash
poetry run python manage.py test
```

## Code Linting et Conformité (Flake8)

Le code de l’API SoftDesk est entièrement conforme aux normes de style de code PEP8, vérifiées avec Flake8. Cela garantit une qualité de code élevée et une meilleure lisibilité.

Pour vérifier la conformité du code, exécutez la commande suivante :

```bash
poetry run flake8
```

## Technologies Utilisées

- Django & Django REST Framework : Backend.
- JWT : Authentification.
- Postman : Documentation des API et tests.
- Poetry : Gestion des dépendances.
- SQLite/PostgreSQL : Base de données.

## Documentation API via Postman

La documentation de l'API SoftDesk est disponible sur Postman :

[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/31282928/2sAY4vhiDB)

## Auteur
**Julien Denzot** - [LuuNa-JD]
