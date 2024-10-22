
# SoftDesk API

SoftDesk est une API RESTful pour la gestion de projets, d'issues, et de commentaires.

## Installation

### 1. Cloner ce dépôt

Clonez ce dépôt en local en utilisant la commande suivante :

```bash
git clone <URL_DU_DEPOT>
cd softdesk_api
```

### 2. Créer et activer un environnement virtuel

Créez un environnement virtuel pour isoler les dépendances du projet.

- Sur MacOS/Linux :

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- Sur Windows :

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Installer les dépendances

Avec l'environnement virtuel activé, installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations de base de données

Exécutez les migrations pour préparer la base de données :

```bash
python manage.py migrate
```

## Lancement

Pour démarrer l'API en local, exécutez la commande suivante :

```bash
python manage.py runserver
```

## Fonctionnalités

- Gestion des utilisateurs et des contributeurs
- Création de projets, d'issues, et de commentaires
- Authentification via Json Web Token (JWT)

## Tests

Vous pouvez utiliser l’outil **Postman** ou **curl** pour tester les différents points de terminaison de l’API.
