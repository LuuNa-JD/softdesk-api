# Documentation de l'API Softdesk

## Authentification

### Obtenir un Token JWT
- **URL** : `/api/token/`
- **Méthode** : `POST`
- **Description** : Permet à un utilisateur de se connecter et d’obtenir un token JWT pour accéder aux endpoints protégés.

#### Paramètres :
- `username` : Nom d'utilisateur.
- `password` : Mot de passe.

#### Exemple de requête :
```json
{
  "username": "testuser",
  "password": "password123"
}
```

#### Réponse :
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

### Rafraîchir un Token JWT
- **URL** : `/api/token/refresh/`
- **Méthode** : `POST`
- **Description** : Permet de rafraîchir le token JWT.

#### Paramètres :
- `refresh` : Token refresh.

#### Exemple de requête :
```json
{
  "refresh": "<refresh_token>"
}
```

#### Réponse :
```json
{
  "access": "<new_access_token>"
}
```

## Utilisateurs

### Créer un utilisateur
- **URL** : `/api/register/`
- **Méthode** : `POST`
- **Description** : Crée un nouveau compte utilisateur.

#### Paramètres :
- `username` : Nom d'utilisateur unique.
- `email` : Adresse e-mail.
- `password` : Mot de passe.
- `age` : Âge de l'utilisateur.
- `can_be_contacted` : Autorisation de contact.
- `can_data_be_shared` : Activation du compte.

#### Exemple de requête :
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123",
  "age": 25,
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

#### Réponse :
```json
{
  "id": 1,
  "username": "newuser",
  "email": "newuser@example.com",
  "age": 25,
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

### Modifier un utilisateur
- **URL** : `/api/profile/update/`
- **Méthode** : `PUT`
- **Description** : Modifie les informations de l’utilisateur connecté.

#### Exemple de requête :
```json
{
  "username": "newusername"
}
```

### Supprimer un compte utilisateur
- **URL** : `/api/profile/delete/`
- **Méthode** : `DELETE`
- **Description** : Supprime le compte de l’utilisateur connecté et toutes les données associées.

#### Exemple de réponse :
```json
{
  "message": "Compte et données associées supprimés avec succès."
}
```

## Projets

### Liste des projets
- **URL** : `/api/projects/`
- **Méthode** : `GET`
- **Description** : Récupère la liste des projets visibles pour l’utilisateur connecté (créateur ou contributeur).

#### Exemple de réponse :
```json
[
  {
    "id": 1,
    "title": "Projet Test",
    "description": "Description du projet",
    "type": "back-end",
    "created_time": "29 October 2024, 11:26",
    "owner": "owner_username"
  }
]
```

### Détails d’un projet
- **URL** : `/api/projects/<project_id>/`
- **Méthode** : `GET`
- **Description** : Récupère les détails d’un projet si l’utilisateur est créateur ou contributeur.

#### Exemple de réponse :
```json
{
  "id": 1,
  "title": "Projet Test",
  "description": "Description du projet",
  "type": "back-end",
  "created_time": "29 October 2024, 11:26",
  "owner": "owner_username"
}
```

### Créer un projet
- **URL** : `/api/projects/`
- **Méthode** : `POST`
- **Description** : Crée un nouveau projet avec l’utilisateur connecté comme propriétaire.

#### Paramètres :
- `title` : Titre du projet.
- `description` : Description du projet.
- `type` : Type de projet (back-end, front-end, iOS, android).

#### Exemple de réponse :
```json
{
  "id": 2,
  "title": "Nouveau Projet",
  "description": "Description du nouveau projet",
  "type": "front-end",
  "owner": "creator_username"
}
```
### Modifier un projet
- **URL** : `/api/projects/<project_id>/`
- **Méthode** : `PUT`
- **Description** : Permet au propriétaire du projet de le modifier.

#### Paramètres :
- `title` : Titre du projet.
- `description` : Description du projet.
- `type` : Type de projet (back-end, front-end, iOS, android).

#### Exemple de réponse :
```json
{
  "id": 1,
  "title": "Projet Modifié",
  "description": "Nouvelle description du projet",
  "type": "front-end"
}
```

### Supprimer un projet
- **URL** : `/api/projects/<project_id>/`
- **Méthode** : `DELETE`
- **Description** : Permet au propriétaire du projet de le supprimer.

#### Exemple de réponse :
```json
{
  "message": "Projet supprimé avec succès."
}
```

## Contributeurs

### Ajouter un contributeur à un projet
- **URL** : `/api/projects/<project_id>/contributors/`
- **Méthode** : `POST`
- **Description** : Permet au propriétaire d’un projet d’ajouter un contributeur.

#### Paramètres :
- `username` : Nom d'utilisateur du contributeur.

#### Exemple de requête :
```json
{
  "username": "contributor_username"
}
```


## Issues

### Liste des issues pour un projet
- **URL** : `/api/projects/<project_id>/issues/`
- **Méthode** : `GET`
- **Description** : Liste toutes les issues d'un projet auquel l'utilisateur est contributeur.

#### Exemple de réponse :
```json
[
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "title": "Issue modifiée par User1",
            "description": "Nouvelle description de l'issue par User1",
            "project": 1,
            "creator_name": "Harry",
            "priority": "HIGH",
            "tag": "FEATURE",
            "status": "Finished",
            "created_time": "30 October 2024, 16:38",
            "assignee_username": "Jeanne"
        },
        {
            "id": 2,
            "title": "Issue créée par User1",
            "description": "Description de l'issue par User1",
            "project": 1,
            "creator_name": "Harry",
            "priority": "MEDIUM",
            "tag": "FEATURE",
            "status": "In Progress",
            "created_time": "30 October 2024, 16:38"
        }
    ],
    "message": "Liste des issues récupérée avec succès."
  }
]
```

### Créer une issue pour un projet
- **URL** : `/api/projects/<project_id>/issues/`
- **Méthode** : `POST`
- **Description** : Crée une nouvelle issue associée à un projet auquel l’utilisateur est contributeur.

#### Paramètres :
- `title` : Titre de l'issue.
- `description` : Description de l'issue.
- `priority` : Priorité de l'issue (LOW, MEDIUM, HIGH).
- `tag` : Type de l'issue (BUG, FEATURE, TASK).
- `status` : Statut de l'issue.
- `assignee` : Nom d'utilisateur de l'assigné.

#### Exemple de réponse :
```json
{
    "id": 3,
    "title": "Issue modifiée par User1",
    "description": "Nouvelle description de l'issue par User1",
    "project": 1,
    "creator_name": "Harry",
    "priority": "HIGH",
    "tag": "FEATURE",
    "status": "Finished",
    "created_time": "30 October 2024, 16:38",
    "assignee_username": "Jeanne",
    "message": "Détails de l'issue récupérés avec succès."
  }
```

### Détails d’une issue
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/`
- **Méthode** : `GET`
- **Description** : Affiche les détails d’une issue pour un projet auquel l’utilisateur est contributeur.

### Modifier une issue
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/`
- **Méthode** : `PUT`
- **Description** : Permet au créateur de l'issue de la modifier.

#### Paramètres :
- `title` : Titre de l'issue.
- `description` : Description de l'issue.
- `priority` : Priorité de l'issue (LOW, MEDIUM, HIGH).
- `tag` : Type de l'issue (BUG, FEATURE, TASK).
- `status` : Statut de l'issue.

### Supprimer une issue
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/`
- **Méthode** : `DELETE`
- **Description** : Permet au créateur de l'issue de la supprimer.

#### Exemple de réponse :
```json
{
  "message": "Issue supprimée avec succès."
}
```


## Commentaires

### Liste des commentaires pour une issue
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/comments/`
- **Méthode** : `GET`
- **Description** : Récupère tous les commentaires d'une issue visible par l'utilisateur.

#### Exemple de réponse :
```json
[
  {
    "id": "uuid",
    "content": "Premier commentaire",
    "creator": "contributor_username",
    "created_time": "29 October 2024, 12:00"
  }
]
```

### Créer un commentaire pour une issue
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/comments/`
- **Méthode** : `POST`
- **Description** : Permet de commenter une issue à laquelle l'utilisateur contribue.

#### Paramètres :
- `content` : Contenu du commentaire.

#### Exemple de réponse :
```json
{
  "id": "uuid",
  "content": "Nouveau commentaire",
  "creator": "contributor_username",
  "created_time": "29 October 2024, 12:15"
}
```

### Détails d’un commentaire
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/`
- **Méthode** : `GET`
- **Description** : Affiche les détails d’un commentaire pour une issue.

### Modifier un commentaire
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/`
- **Méthode** : `PUT`
- **Description** : Permet au créateur d'un commentaire de le modifier.

#### Paramètres :
- `content` : Contenu du commentaire.

### Supprimer un commentaire
- **URL** : `/api/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/`
- **Méthode** : `DELETE`
- **Description** : Permet au créateur d'un commentaire de le supprimer.

#### Exemple de réponse :
```json
{
  "message": "Commentaire supprimé avec succès."
}
```


## Erreurs et Réponses

### Codes de réponse standard :
- `200 OK` : Succès de la requête.
- `201 Created` : Création réussie.
- `204 No Content` : Suppression réussie.
- `400 Bad Request` : Requête mal formée.
- `401 Unauthorized` : Authentification requise.
- `403 Forbidden` : Accès refusé.
- `404 Not Found` : Ressource non trouvée.

### Exemples de messages d’erreur personnalisés :
- **Non-Contributeur** : `{"error": "L'utilisateur n'est pas contributeur de ce projet."}`
- **Non-Propriétaire** : `{"error": "Seul le propriétaire peut ajouter des contributeurs."}`
- **Non-Autorisé** : `{"error": "Vous devez être authentifié pour accéder à cette ressource."}`

### Utilisation recommandée :
Pour une expérience optimale, assurez-vous d'obtenir et de rafraîchir régulièrement le token JWT pour garder l’accès aux endpoints sécurisés.
