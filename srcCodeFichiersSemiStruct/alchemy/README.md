# App de gestion des étudiants (SQLAlchemy)

## Installation et exécution

### Méthode 1: Avec Docker (recommandé)

1. Assurez-vous que Docker est installé et démarré.

2. Construisez et lancez l'app :
```bash
docker-compose up --build
```

L'app sera accessible sur `http://localhost:5000`.

### Méthode 2: Installation locale

1. Créez un environnement virtuel et installez les dépendances:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Lancez l'app:

```bash
python run.py
```

L'app démarrera sur `http://127.0.0.1:5000/`. La base SQLite `alchemy.db` sera créée automatiquement.

## Documentation API

Accédez à la documentation SwaggerUI à l'adresse : `http://127.0.0.1:5000/apidocs/`

Ou via le lien `/docs` dans l'app.

## Structure du projet

- `run.py` : exécuteur qui initialise la DB et démarre Flask
- `app/__init__.py` : création de l'app et de `db` (SQLAlchemy)
- `app/models.py` : modèle `Etudiant` et fonctions d'accès
- `app/views.py` : routes et logique
- `app/templates/` : `index.html`, `new.html`, `login.html`
- `Dockerfile` : configuration Docker
- `docker-compose.yml` : orchestration Docker
