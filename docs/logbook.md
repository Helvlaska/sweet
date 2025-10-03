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

- [X] Création de la classe abstraite BaseClass (CRUD générique + timestamps).
- [ ] Création de la classe User (attributs, sécurité mdp).
- [ ] Ajouter validation (regex : email, mdp, etc).
- [ ] Configuration migration + premier flask db init/migrate/upgrate.

### 🪲 Bugs / difficultés rencontrées

- Réflexion sur la sécurisation des données passées en JSON notamment pour le mdp.
  - Prise de renseignement sur "exclude" dans une fonction to_dict().
- Journée en exterieur : Rennes.
  - Focus légé sur le code de Sweet.

### 🔀 SCM (branches & commits)

- Branches :
  - Mise à jour du journal de bord → `logbook`.
  - Ajout d'outils réutilisables dans ma toolbox → `toolbox_backend`.
  - Branche tirée pour la création de BaseModel et la création de la classe User.

- Commits :

  - 📝 (toolbox_backend/): Add tools naming, regex and class template
  - 📝 (docs/logbook.md): Add logbook and set objectives for day 2 week 1

### 🧪 QA (tests faits)

- [ ] Pas de tests fais sur cette session de travail.

### 💡 Notes / décisions

- Intégration de "exclude" pour la fonction to_dict(), cohérent avec la volonté de Sweet d'être une application sécurisée.
- Poursuite des objectifs du jour 2 en jour 3, amplitude horaire allongée pour respecter les objectifs du planning définis en amont.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - La création de BaseModel inspirée de la BaseModel du HBnB s'est bien passée, elle a même été améliorée.
  - Je me challenge sur la sécurisation de l'application, ce qui n'est pas mon point fort de base, je monte en compétence et reflexe.
- ⚠️ À améliorer :
  - Je dois me concentrer sur mon code lorsque je suis en groupe. Les interactions sociales sont importantes mais elle ne doivent pas nuire au bon déroulement du travail en cours.

---

## Jour 3 – Base Classe + Routes Auth (01/10/25)

### 🎯 Objectifs du jour

- Création de la classe User (attributs, sécurité mdp).
- Ajouter validation (regex : email, mdp, etc).
- Configuration migration + premier flask db init/migrate/upgrate.
- Mise au point des routes Auth (/auth/register, /auth/login, /auth/logout).
- Générer JWT + refresh token.
- Gérer cookies sécurisés (httpOnly).

### ✅ Réalisé

- [X] Création de la classe User (attributs, sécurité mdp).
- [X] Ajouter validation (regex : email, mdp, etc).
- [ ] Configuration migration + premier flask db init/migrate/upgrate.
- [ ] Mise au point des routes Auth (/auth/register, /auth/login, /auth/logout).
- [ ] Générer JWT + refresh token.
- [ ] Gérer cookies sécurisés (httpOnly).

### 🪲 Bugs / difficultés rencontrées

- Prise de renseignements sur les conventions moderne du nombre de char / champs :
  - les standards IETF, ISO, ICAO (email, nom dans passeport, etc.).
  - les pratiques banques / assurances / santé.
  - les bases d’utilisateurs (Salesforce, Google, Facebook, etc.).
  - les retours des cas « limites » (Malgache, Indonésien, Islandais, etc.).
- Déterminer si le champ "role" est bien un Enum.
  - Oui il restera en Enum car plus robuste.
- Déterminer si un user supprime son compte est ce que :
  - Ses données personnelles sont supprimées, sauf ces posts et commentaires sur le forum?
    - Cette solution à été choisis, car si dans le forum les commentaires et les posts sont supprimés ils perdrons potentiellement du sens. Par contre le username sera modifié (User deleted, Unknow user, etc à déterminer).
  - L'ensemble de des données sont supprimées? ❌
- Réflexion sur quels champs de la classe User passer en privé ou en publique :
  - Champs privés : Les champs qui servent à la connexion et ceux qui contiennent des données personnelles (age, genre, taille, etc).
  - Champs publiques : Le reste.
- Centralisation des regex
  - Code répétitif sur les validations de valeur de champ → Possibilité de créer une fonction réutilisable.
  - Création d’un fichier validators.py qui contient :
    - une fonction générique is_valid(value, pattern).
    - une fonction génératrice make_text_pattern(min_length, max_length).
    - des constantes regex (EMAIL_PATTERN, USERNAME_PATTERN, etc.).
- Approche whitelisting → Plutôt que de créer une multitude de regex personnalisées pour chaque champ, en créer une seule mais modulable.
  - Autoriser uniquement les caractères attendus (lettres, chiffres, accents, quelques ponctuations).
  - Objectif : empêcher les injections (SQL/XSS) dès la validation des champs.
- Usage des @property / @setter
  - Les champs sensibles (email, username, password, role, etc.) → privés (_email, _username, etc.) et exposés via @property.
  - Setters = validations systématiques (type, vide, format, bornes).
    - Username → regex inspirée de la pattern de GitHub/twitter.
    - Date_of_birth → réflexion sur le bornage des dates : pas après la date du jour mais pas avant 1900.
    - Changement du nom de l'attribut "sex" remplacé par "gender", quitte à faire une application inclusive autant l'être dans son code.
    - Taille → réflexion sur le bornage minimum de la taille, Sweet pourrait très bien être utilisé par des parents qui on un bébé diabétique, or la taille est importante dans le calcul de l'IMC, au lieu d'un bornage minimum à 50 cm, décision de le faire passer à 30 cm.
    - Profil_picture → Setter construit dans l'optique d'un stockage de fichier de type image, pousser la réflexion lors de la manipulation par l'API.
    - Role → Pour savoir si c'est un admin ou un user, envie de simplifier avec un boolean is_admin, mais pour la suite de Sweet, il vaut mieux un Enum, mais je dois le sécuriser dans l'API.
- Logs (app.logger) anticipés pour suivre les validations/rejets.
- Demain trancher si je mets un __repr__ dans mon module User.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la création de la classe User. → `user-model`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 3 week 1
  - ✨ (models/user.py): Add User class with attributes and validation methods
  - ✨ (utils/validators.py): Add validation functions and regex for text, username, email, and password fields
  - 📝 (docs/logbook.md): Update progress for day 3 week 1

### 🧪 QA (tests faits)

- [ ] Pas de tests fais sur cette session de travail.

### 💡 Notes / décisions

- Retard pris en jour 2, non rattrapé en jour 3, mais le module user.py est presque fini. Demain se sera de la connexion et de la configuration, il est probable de gagner du temps à ce moment là.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - La classe User c'était LE module le plus long et avec le plus d'attributs (13!), et je l'ai fais en une journée.
  - Belle idée de m'être préparé des tools dans ma boite à outils backend, j'ai gagné beaucoup de temps dans la mise en place des différentes parties du module. Un travail bien préparé est un travail bien fait ! ça m'a aussi permise de me concentrer et de réfléchir sur les attributs que je pensais simple de prime abord mais en fait il y a des subtilités (exemple: les dates).
  - Ajouter les logs maintenant plutôt que après ça va être un gain de temps et m'évite de retravailler encore sur ce mega module.
  - J'ai pus apprendre pleins de chose sur les conventions internationales de remplissage de champs.
  - Pousser ma réflexion sur les utilisateurs de Sweet, leur culture, leur âge, comment l'application peu au mieux matcher avec leur vie.
  - La centralisation des certaines fonctions redondantes, je n'étais pas à l'aise mais finalement ça s'est bien passé.
- ⚠️ À améliorer :
  - Se renseigner sur la gestion des différents champs avec un setter (date)
  - La gestion du temps, même si là c'était un gros morceau, je risque de devoir travailler ce w.e, et de ne pas pouvoir préprer mes outils pour la semaine prochaine.

---

## Jour 4 – Migration + Route Auth (02/10/25)

### 🎯 Objectifs du jour

- Configurer migrations + premier flask db init/migrate/upgrade.
- Matin : mise au point des routes Auth (/auth/register, /auth/login, /auth/logout).
- Générer JWT + refresh token.
- Gérer cookies sécurisés (httpOnly).

### ✅ Réalisé

- [X] Configurer migrations + premier flask db init/migrate/upgrade.
- [ ] Mise au point des routes Auth (/auth/register, /auth/login, /auth/logout).
- [ ] Générer JWT + refresh token.
- [ ] Gérer cookies sécurisés (httpOnly).

### 🪲 Bugs / difficultés rencontrées

- Formation sur l'utilisation de la migration avec Flask-Migrate et migration en elle même.
  - BUG refonte du module de la BaseModel par ce que je n'avais pas anticipé la migration.
  - J'ai aussi appris que pour faire une migration propre je dois :
    - Ajouter dans models/__init__.py l'import de la classe.
    - Dans mon terminal :
      - Rappeler à mon app où chercher mon fichier d'exécution → export FLASK_APP=run.py
      - Effectuer la migration → flask db migrate -m "create tableName table"
      - Lancer la mise à jour de la db → flask db upgrade

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la migration de la classe User. → `user-model`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 4 week 1
  - ♻️ (models/base.py): Refactor BaseModel to use SQLAlchemy ORM, update timestamp handling, and improve to_dict method
  - ♻️ (models/user.py): Reorganize imports to improve readability and code structure
  - ➕ (requirements.txt): Add Flask-JWT-Extended, Flask-Bcrypt, and python-dotenv dependencies
  - ♻️ (app/init.py): Refactor create_app function to use consistent variable naming and initialize bcrypt
  - 📝 (docs/logbook.md): Update progress for day 4 week 1

### 🧪 QA (tests faits)

- [X] Vérification que la migration à fonctionné.

### 💡 Notes / décisions

- Même si j'ai anticipé en amont, il faut que je prennes en compte et plannifies des plages horaire pour gérer le retard.
  - Le jour 6 ou 7 de la semaine 1 : Mise en place de sessions de travail plus longues que celles planifiées + Modification du planning de la semaine 2 en prévoyant une journée pour gérer les imprévus de la semaine en cours.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Malgré un problème sur le fichier de ma BaseModel qui n'était pas construite en vu d'une migration, la migration en elle même s'est bien passé.
  - Je suis agréablement surprise par cet outil que je trouve pratique, travaillons mieux en faisant le moins.
- ⚠️ À améliorer :
  - J'avais anticipé certaines choses, mais je dois prendre en compte les imprévus.
  - Je dois ajouter à mon planning des sessions de travail pour gérer les imprévus.
