# Journal de bord – Semaine 1

## Jour 1 – Backend socle (29/09/25)

### 🎯 Objectifs du jour

- Mettre en place le journal de bord.
- Créer et organiser GitHub Projects.
- Préparer l’arborescence backend.
- Initialiser Flask avec une config de base.
- Mettre en place l’environnement virtuel et les dépendances.
- Vérifier le lancement de l’app.

### ✅ Réalisé

- [X] Journal de bord mis en place.
- [X] GitHub Projects configuré :
  - Draft = tâches rapides.
  - New issue = tâches complexes (avec sous-tâches).
- [X] Arborescence backend créée.
- [X] Environnement virtuel installé + `requirements.txt` généré.
- [X] Initialisation de Flask (`__init__.py`, `run.py`).
- [X] Fichier `config.py` :
  - Configuration globale.
  - Développement local.
  - Tests.
  - Production.
- [X] Fichier `.env` créé pour sécuriser les clés (`SECRET_KEY`, etc.) → ajouté dans `.gitignore`.
- [X] Lancement de l’app → `/ping` répond correctement.

### 🪲 Bugs / difficultés rencontrées

- Problème d’interpréteur Python qui ne pointait pas sur mon `venv` → corrigé via réglage de VSCode.

### 🔀 SCM (branches & commits)

- Branches :
  - Création du journal de bord → `logbook`.
  - Création de l'arborescence → `setup-backend`.

- Commits :

  - 📝 (docs/logbook.md): Add logbook and set objectives for day 1 week 1
  - ✨ (backend/): Initial Flask setup with config, env and healthcheck route
  - 📝 (docs/logbook.md): Update progress for day 1 week 1

### 🧪 QA (tests faits)

- [X] Faire tourner l'application Flask.

### 💡 Notes / décisions

- Mise en place d'un fichier `.env` pour sécuriser mes clés.
- Configuration de l'application en prévisions d'une utilisation de `Docker` pour lancer le backend et le frontend.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - J'ai remplis tout mes objectifs de la journéee dans le temps que je me suis fixé → Bon calibrage de ma charge de travail /jour.
  - Utiliser un journal et bord et GitHub projects en complément.
  - Mon arborescence est comme je l'avais imaginée, propre, solide, et bien décomposée.
  - J'ai pus calibrer mes fichiers d'initialisation de l'application de façon à ce qu'ils soient évolutif.
  - La sécurisation est un point important de Sweet, je penses que le fichier `.env` était une bonne idée en plus d'être une bonne pratique. J'ai pus me former dessus en conditions réelles.
- ⚠️ À améliorer :
  - La création des fichiers de configuration et d'initalisation d'application Flask c'est pas encore acquis.
    - Créer un template de base ?
  - Synchronisation des branches documentaires :
    - Mieux utiliser `git rebase` pour éviter les commits de merge parasites.
  - Automatisation du lancement de l’app :
    - Créer un alias ou un script `start.sh` pour éviter de retaper les commandes.

---

## Jour 2 – Base Classe (30/09/25)

### 🎯 Objectifs du jour

- Création de la classe abstraite BaseClass (CRUD générique + timestamps).
- Création de la classe User (attributs, sécurité mdp).
- Ajouter validation (regex : email, mdp, etc).
- Configuration migration + premier flask db init/migrate/upgrate.

### ✅ Réalisé

- [ ] Création de la classe abstraite BaseClass (CRUD générique + timestamps).
- [ ] Création de la classe User (attributs, sécurité mdp).
- [ ] Ajouter validation (regex : email, mdp, etc).
- [ ] Configuration migration + premier flask db init/migrate/upgrate.

### 🪲 Bugs / difficultés rencontrées

-

### 🔀 SCM (branches & commits)

- Branches :
  - Mise à jour du journal de bord → `logbook`.
  - Ajout d'outils réutilisables dans ma toolbox → `toolbox_backend`.

- Commits :

  - 📝 (toolbox_backend/): Add tools naming, regex and class template
  - 📝 (docs/logbook.md): Add logbook and set objectives for day 2 week 1

### 🧪 QA (tests faits)

- [ ]

### 💡 Notes / décisions

-

### 🔄 Rétro rapide (fin de journée)
