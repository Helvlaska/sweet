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

---

## Jour 5 – Mise au point de la route Auth (03/10/25)

### 🎯 Objectifs du jour

- Mise au point des routes Auth (/auth/register, /auth/login, /auth/logout, /auth/reset, /auth/profile).

### ✅ Réalisé

- [X] Route /auth/register
- [X] Route /auth/login
- [X] Route /auth/logout
- [X] Route /auth/reset
- [X] Route /auth/profile

### 🪲 Bugs / difficultés rencontrées

- Pas de difficultés particulières aujourd'hui.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des routes Auth. → `user-model`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 5 week 1
  - ♻️ (app/init.py): Improve readability by adding comments and reorganizing blueprint registration
  - ✨ (utils/responses.py): Add functions to standardize JSON success and error responses
  - ✨ (routes/auth.py): Implement authentication routes for registration, login, logout, password reset, and profile management
  - 📝 (docs/logbook.md): Update progress for day 5 week 1

### 🧪 QA (tests faits)

- [ ] Pas de tests ce jour.

### 💡 Notes / décisions

- Formation et utilisation de Blueprint de flask.
  - Ajout dans app/__init__.py de mon premier Blueprint → auth_bp.
- Renseignement sur le process classique d'un "mot de passe oublié".
  - Je vais le faire en deux fonctions :
    - Une pour créer la requête de modification avec un token ephémère.
    - Une autre pour vérifier ce dit token avec une double vérification du nouveau mot de passe.
- Mise en place des routes et fonctions sans les remplir, attente du fichier services/auth_service.py.
  - Ajout en commentaire dans mes fonctions de la logique de vérification pour chacune, comme ça j'ai pus repérer les vérifications redondantes, je pourrais ainsi faire des fonctions réutilisables.
- Ajout d'un fichier qui contient mes fonctions de standardisation de mes jsonify.
  - Je trouve ça plus propre, mais par contre je dois pas tromper dans l'ordre des arguments, je me suis crée un template pour ne pas me tromper.
  - Je l'ai appelé utils/reponses.py j'espère que c'est un nom suffisament parlant.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - J'ai appris à créer et utiliser des Blueprint.
  - J'ai quand même bien avancé sur les routes d'authentifications, malgré que j'étais en évènement pro toute la matiné.
  - Mes fonctions succes_response et error_response correspondent tout à fait à ma logique de traçabilité, mes logger aussi je les trouve bien construits.
- ⚠️ À améliorer :
  - L'ensemble de la journée c'est bien passé, à part mon retard de planning que je vais ratrapper en jour 6 et 7, je n'ai rien à documenter.

---

Template du logbook:

## Jour 6 – Auth (04/10/25)

### 🎯 Objectifs du jour

- Boîte à outils Auth (services/auth_service.py).
  - Gestion des champs (validation).
  - Gestion du mot de passe.
  - Gestion des utilisateurs (DB).
- Routes à implémenter (routes/auth.py)
  - Authentification.

### ✅ Réalisé

- [ ] Boîte à outils Auth (services/auth_service.py)
  - [X] Gestion des champs (validation)
  - [X] Gestion du mot de passe
  - [X] Gestion des utilisateurs (DB)

- [ ] Routes à implémenter (routes/auth.py)
  - [ ] Authentification
    - [X] Register (POST /register)
    - [ ] Login (POST /login)
      - [X] Champs obligatoires + validation.
      - [X] Vérif user (email/username).
      - [X] Vérif mot de passe.
      - [ ] Génération JWT + retour JSON.
      - [X] Logger + success_response.


### 🪲 Bugs / difficultés rencontrées

- Grosses difficultés sur la gestion et génération de token, pour rappel dans mon MVP lors de la connexion :
  - Soit l'utilisateur choisis une connexion classique qui génère un acces_token de 24h.
  - Soit l'utilisateur à la possibilité lors de sa connexion de cocher une case "se souvenir de moi", elle génère alors un accès_token ET un refresh_token de 48h.
  - Ensuite les tokens sont ajoutés aux cookies protégés.
  Je dois me former sur ce toogle de génération de token et aussi sur les cookies.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des routes Auth. → `user-model`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 6 week 1
  - ✨ (services/auth_service.py): Add functions for user data validation, login data validation, user creation, and user authentication
  - ♻️ (routes/auth.py): Refactor register route to utilize validation and user creation functions
  - 📝 (docs/logbook.md): Update progress for day 6 week 1

### 🧪 QA (tests faits)

- [ ] Pas de tests ce jour.

### 💡 Notes / décisions

- Les setter de ma classe User m'ont grandement facilité la tâche de vérification, je vais utiliser la même logique pour mes autres classes et routes

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - La facilité de validation des champs, me rassure sur mon choix de les avoir mis dans ma classe.
- ⚠️ À améliorer :
  - Prévoir un demi-journée pour se former sur des nouveaux concepts, c'est chronophage et vraiment le temps passe beaucoup trop vite, surtout pour rester conforme aux quatre semaines de délais.

---

## Jour 7 – Auth (suite) (05/10/25)

### 🎯 Objectifs du jour

- Boite à outils Auth (services/auth_service.py)
  - Gestion des tokens.
- Routes à implémenter (routes/auth.py)
  - Authentification → Génération de tokens
  - Reset Password.

### ✅ Réalisé

- [ ] Boîte à outils Auth (services/auth_service.py)
  - [X] Gestion des tokens
    - [X] Générer un access_token + refresh_token pour un utilisateur.
    - [X] Générer un token temporaire pour un reset de mot de passe.
    - [X] Vérifier si un token de reset est valide et non expiré.
    - [X] Invalider un token de reset après usage.
    - [X] Nettoyer/invalider les cookies et tokens lors du logout.

- [ ] Routes à implémenter (routes/auth.py)
  - [X] Authentification
    - [X] Login (POST /login)
      - [X] Génération JWT + retour JSON.
      - [X] Logger + success_response.
    - [X] Logout (POST /logout)
      - [X] Nettoyer cookies/tokens.
      - [X] Logger + success_response.
  - [X] Reset Password
    - [X] Reset Request (POST /reset)
      - [X] Vérifier email fourni et user existe.
      - [X] Générer token reset (MVP → retour JSON).
      - [X] Logger + success_response.
    - [X] Reset Confirm (PUT /reset/< token>)
      - [X] Vérifier token valide/non expiré.
      - [X] Vérifier new_password.
      - [X] Hash + update DB.
      - [X] Invalider token.
      - [X] Logger + success_response.
    - [X] Update Password connecté (PUT /reset)
      - [X] Vérifier JWT valide.
      - [X] Vérifier old_password correct.
      - [X] Vérifier new_password conforme.
      - [X] Hash + update DB.
      - [X] Logger + success_response.

### 🪲 Bugs / difficultés rencontrées

- La partie la plus difficile aujourd'hui à été les services pour la réinitialisation du password.
  - Est ce que je fais un reset du niveau d'un MVP, alors que je code comme une application pro depuis le départ ?
  - Est ce que ce n'est pas une perte de temps et d'énergie alors que je ne peux pas encore tester ?
  - J'ai eu des difficultés pour comprendre et visualiser le contenu de mes réponse :
    - est ce que c'est un tuple ?
    - est ce que c'est un dictionnaire ?
    - est ce que c'est une valeur simple ?
    Quelques confusions finalement mais qui m'ont fait retravailler mes types de réponses.
- J'ai un énorme fichier de services (services/auth_service.py), j'ai eu vraiment peur de trop m'étaler et du coup de perdre du temps, mais finalement la mise en place de mes routes a été grandement facilitée (merci moi, d'avoir prévus).
- J'ai eu des problèmes de type de donnée à cause de Pylance, j'ai dus utiliser # type: ignore, sur certaines lignes.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des routes Auth. → `user-model`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 7 week 1
  - ➕ (app/init.py): Add JWT configuration for token management and secure cookies
  - ➕ (requirements.txt): Add Flask-Mail for email management
  - ➕ (app/init.py): Add Flask-Mail for email management
  - ♻️ (models/user.py): Add default value for the _first_login field
  - ♻️ (utils/responses.py): Add a 'data' parameter to the error_response function to include additional data in error responses
  - ♻️ (routes/auth.py): Refactor authentication routes to use auth_service methods and improve error handling
  - ♻️ (services/auth_service.py): Refactor user authentication and password reset functionalities; add email sending for password reset requests
  - 📝 (docs/logbook.md): Update progress for day 7 week 1

### 🧪 QA (tests faits)

- [ ] Pas de tests ce jour.

### 💡 Notes / décisions

- J'ai codé mon reset password comme pour une vraie application déployable, j'ai dépassé un peu mon MVP, mais quitte à me former autant le faire pour que ça me soit utile en entreprise. C'est un risque.
- J'ai eu la possibilité de rendre modulable certains services, mais j'ai encore besoin d'avoir des fonctions séparées qui font qu'une seule chose pour gérer et comprendre lors de la construction de mes routes. Il faut que je prévois un temps pour l'opptimisation de fonctions. (Si j'ai pas le temps, ce n'est pas grave, ça reste fonctionnel).

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - J'ai encore appris beaucoup de choses pendant cette session de travail (tokens, cookies, reset password).
  - Je me félicite tout les jours de ma classe User → un gain de temps incroyable surtout pour la vérification des champs, je vais m'en inspirer pour le reste de mes classes.
  - La partie authentification pure est enfin terminée.
- ⚠️ À améliorer :
  - Je finis la semaine avec du retard sur mon planning.
    - J'ai bon espoir que mes sessions de travail cette semaine 1 me permettrons de gagner du temps la semaine 2.
  - J'ai un manque flagrant de connaissance sur les outils de Flask.
    - J'ai ajouté dans ma to do de me former sur des librairies utiles type jwt ou Flask_jwt_extended.
  - Je ne suis pas à l'aise avec l'authentification, l'utilisation des token, et des cookies.
    - Je penses que ça va venir avec l'expérience et surtout beaucoup de pratique.
  - Je me rends compte que j'ai des lacunes sur les tuples, dictionnaires, listes.
    - Refaire des exercices ne me ferais pas de mal, il faut que je trouve du temps.

---

## Jour 8 – Auth (fin) (06/10/25)

### 🎯 Objectifs du jour

- Finir les 4 fonctions manquantes du fichier services/auth_service.py.
- Finaliser les routes correspondantes.
- Vérifier la cohérence avec les tokens JWT
- Tests manuels Postman

### ✅ Réalisé

- [ ] Boîte à outils Auth (services/auth_service.py)
  - [X] Gestion du profil
    - [X] Récupérer l’utilisateur courant via JWT (get_jwt_identity).
    - [X] Retirer les champs sensibles avant de retourner le profil (mot de passe, tokens).
    - [X] Vérifier la validité des champs envoyés lors d’une mise à jour de profil.
  - [ ] Sécurité & rôles
    - [ ] Assigner le rôle user par défaut à l’inscription.
    - [ ] Vérifier les accès selon le rôle (user/admin).

- [X] Routes à implémenter (routes/auth.py)
  - [X] Gestion du profil
    - [X] Show Profile (GET /profile)
      - [X] Vérifier JWT valide.
      - [X] Charger user.
      - [X] Nettoyer données sensibles.
      - [X] Logger + success_response.
    - [X] Update Profile (PUT /profile)
      - [X] Vérifier JWT valide.
      - [X] Valider champs (regex, unicité email).
      - [X] Update DB.
      - [X] Logger + success_response.
  - [ ] Sécurité & Qualité
    - [ ] Ajouter rôle user par défaut à l’inscription.
      - [ ] Vérifier rôle admin seulement via DB.
      - [X] Centraliser logs (app.logger).
      - [ ] Créer exceptions custom dans exceptions.py.
      - [ ] Remplacer certains error_response par exceptions custom si besoin.

### 🪲 Bugs / difficultés rencontrées

- Mes error_response et success_response font beaucoup de bruit dans mon code.
  - Lors de ma phase de tests (elle se termine jour 2), je dois déterminer si elles mes sont vraiment utiles pour le debugue ou si je peux me contenter des logger.
- Pylance est un problème récurant dans mon code, il se perd dans les types quand mes fonctions return, déjà que c'est difficile de penser à tout, mais si en plus je dois typer mes fonctions je ne m'en sortirais jamais, ou en tout cas pas dans le temps imparti. (Note à moi-même : ça me permettrait sans doute de réviser les tuple, liste et dictionnaire 👀🥲)

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des routes Auth. → `user-model`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 1 week 2
  - ♻️ (app/init.py): Add logging configuration and disable CSRF protection for JWT cookies during testing
  - ♻️ (models/user.py): Refactor User model, update date_of_birth handling to allow nullable values and improve error logging for date format validation
  - ♻️ (routes/auth.py): Refactor authentication routes to improve user profile handling and logging; sanitize user profile data and streamline response messages
  - ♻️ (services/auth_service.py): Refactor user data validation and profile management; improve error handling and logging for user creation and profile updates
  - ✨ (utils/logging.py): Implement code changes to enhance functionality and improve performance
  - 📝 (docs/logbook.md): Update progress for day 1 week 2

### 🧪 QA (tests faits)

- [ ] Tests
  - [ ] Tests manuels (Postman)
    - [X] register → login → logout.
    - [ ] reset password (oublié).
    - [ ] reset password (connecté).
    - [ ] profil (GET/PUT).
    - [ ] rôles (user/admin).
  - [ ] Tests unitaires (Pytest)
    - [X] Création user.
    - [X] Login.
    - [ ] Reset password.

### 💡 Notes / décisions

- Pendant les premiers tests, je me rends compte que je regarde d'avantage mes logger et mes sorties en console, plutôt que mes responses, d'autant que j'ai beaucoup de problèmes en ce qui concerne les type de response.
  - Je vais attendre la fin des tests pour prendre une décision.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Je me suis formée à Postman, autant la toute première fois je n'avais rien compris, autant aujourd'hui, j'ai pris le temps de bien comprendre, d'expérimenter, et vraiment c'est une belle (re)découverte.
  - J'ai enfin terminé mes fichiers pour l'authentification, il ne me reste qu'une partie des tests et la gestion de user/admin, mais c'est gérable pour demain soir.
  - Même si je tatonne encore, je suis contente, par ce que je trouve ma façon de coder, ou en tout cas celle que je comprends, et qui me convient.
- ⚠️ À améliorer :
  - Des difficultés mais ça à été une bonne journée.

---

## Jour 9 – Tests Auth + Glycemia/Weight (07/10/25)

### 🎯 Objectifs du jour

- Tests /reset et /profile
- Créer les classes Glycemia et Weight dans /models
  - Implémenter leurs services CRUD + routes /data/glycemia et /data/weight
  - Tests Postman (add, get, range)

### ✅ Réalisé

- [ ] Bloc Glycemia et Weight
  - [X] Création classe Glycemia
  - [ ] Implémenter services CRUD
  - [ ] Implémenter routes /data/glycemia
  - [X] Création classe Weight
  - [ ] Implémenter services CRUD
  - [ ] Implémenter routes /data/weight

### 🪲 Bugs / difficultés rencontrées

- Pas de difficultés particulières aujourd'hui.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des routes Auth. → `user-model`. → Branche mergée et supprimée.
  - Mise à jour du journal de bord → `logbook`.
  - Branche tirée pour la gestion des classes Glycemia et Weight → `glycemia-weight-module`

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 2 week 2
  - 🧪♻️ (routes/auth.py): Refactor code following Postman testing
  - 🧪♻️ (services/auth_service.py): Refactor code following Postman testing
  - 🧪♻️ (models/user.py): Refactor code following Postman testing
  - ➕ (utils/logging.py): Implement code changes to enhance functionality and improve performance
  - 🔀 (user-model → main): Merge user-model working branch into main
  - ✨ (models/glycemia.py): Add Glycemia class with glucose level validation
  - ✨ (models/weight.py): Add Weight class with weight validation
  - 📝 (docs/logbook.md): Update progress for day 2 week 2

### 🧪 QA (tests faits)

- [X] Tests /auth
  - [X] reset password (oublié).
  - [X] reset password (connecté).
  - [X] profil (GET/PUT).
  - [X] rôles (user/admin)
- [ ] Tests /glycemia /weight
  - [ ] Tests sur Glycemia
  - [ ] Tests sur Weight

### 💡 Notes / décisions

- Maintenant que les tests sont terminés pour la classe User, ainsi que pour l'authentification, je vais arrêter d'utiliser mes responses formatées, presque toutes mes erreurs lors des tests étaient liées à elles.
- J'ai terminé aujourd'hui les classes Glycemia et Weight, elles ont étés extrêmement rapides à faire. La classe User était définitivement la plus longue.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Je peux enfin dire que l'authentification est terminée, c'était la moitié de mon backend finalement en terme de charge de travail. Je suis très contente de l'avoir finie.
  - Même si il me reste presque 10x classes à faire, elles sont très rapide à faire, dans mon planning j'ai prévus d'en faire 2/jour, je penses que c'est planning est jouable.
- ⚠️ À améliorer :
  - J'arrête l'utilisation de mes responses personnalisées.
  - Je n'ajoute que mes logs pour debuguer, c'est largement suffisant.

---

## Jour 10 – Glycemia/Weight (08/10/25)

### 🎯 Objectifs du jour

- Implémenter les services CRUD pour les classes Glycemia et Weight
- Implémenter les routes /data/glycemia et /data/weight
- Tests Postman (add, get, range)
- Créer les classes Activity et Meal

### ✅ Réalisé

- [ ] Implémenter services CRUD
- [ ] Implémenter routes /data/glycemia
- [ ] Implémenter services CRUD
- [ ] Implémenter routes /data/weight
- [ ] Création classe Activity
- [ ] Création classe Meal

### 🪲 Bugs / difficultés rencontrées

- Je me suis rendue compte pendant l'élaboration de mes services pour la classe Glycemia, que je n'avais pas pensé dans mon diagramme de classe à toutes la gestion concernant les dates:
  - J'ai une date de création → Elle ne doit pas être modifiée, elle me sert de point de repère dans ma BDD.
  - J'ai une date de modification → Elle non plus ne bouge pas, elle me sert à tracer les mouvement dans ma BDD par rapport à la date de création.
  - Mais il me manquait une date, que je pourrais manipuler et modifier au besoin pour pouvoir regrouper toutes les données pour une journée ou pour une période (date à date), j'ai mis en place une 3e date pour cela.

### 🔀 SCM (branches & commits)

- Branches :
  - Mise à jour du journal de bord → `logbook`.
  - Branche tirée pour la gestion des classes Glycemia et Weight → `glycemia-weight-module`.
  - Branche tirée pour la gestion des classes Activity et Meal → `activity-meal-module`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 3 week 2
  - ➕ (app/init.py): Register data blueprint for improved routing
  - ➕ (models/init.py): Import Glycemia and Weight classes for model accessibility
  - ➕ (models/base.py): Add entry_date column to record the entry date
  - ➕ (models/glycemia.py): Add user_id column to associate glycemia records with users
  - ➕ (models/user.py): Add weight relationship to User model for weight tracking
  - ➖ (routes/auth.py): Remove unnecessary import of get_jwt_identity
  - ✨ (routes/data.py): Add routes for managing glycemia and weight data
  - ✨ (services/data_service.py): Add functions to validate and create glycemia entries
  - 📝 (docs/logbook.md): Update progress for day 3 week 2

### 🧪 QA (tests faits)

- [ ] Tests /glycemia /weight
  - [ ] Tests sur Glycemia
  - [ ] Tests sur Weight

### 💡 Notes / décisions

- Mise en place d'une troisième date dans la BaseModel qui s'héritera dans toutes les classe, afin de me permettre de manipuler et regrouper mes données.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - J'ai pus trouver une solution très simple à mon problème de date. La mise en place à été d'autant facilitée par ce que mes classes sont bien construites.
  - J'ai sans doute trouvé une solution à mon problème de Pylance qui ne reconnait pas mes types quand je manipule de la donnée, je dois tester demain.
- ⚠️ À améliorer :
  - Je prends du retard sur mon planning, mais je ne suis pas inquiète. Mais je dois faire attention, dans mon planning le front commence la semaine prochaine.
  - J'avais oublié que lorsque je fais des relations entre les classes, il faut que je déclare la liaison dans ma classe one mais aussi dans les classes many.
  - J'ai beaucoup de fonctions déclarées qui sont censées me faciliter la vie, mais je les oublies, je penses que je vais pouvoir optimiser mon code en ce sens, je dois prendre un temps pour voir et corriger ça.

---

## Jour 11 – Glycemia/Weight services + routes (09/10/25)

### 🎯 Objectifs du jour

- Implémenter les services CRUD pour les classes Glycemia et Weight
- Implémenter les routes /data/glycemia et /data/weight
- Tests Postman (add, get, range)
- Créer les classes Activity et Meal

### ✅ Réalisé

- [X] Implémenter services CRUD glycemia
- [X] Implémenter routes /data/glycemia
- [X] Implémenter services CRUD weight
- [X] Implémenter routes /data/weight
- [ ] Création classe Activity
- [ ] Création classe Meal

### 🪲 Bugs / difficultés rencontrées

- Pas de difficultés aujourd'hui

### 🔀 SCM (branches & commits)

- Branches :
  - Mise à jour du journal de bord → `logbook`.
  - Branche tirée pour la gestion des classes Glycemia et Weight → `glycemia-weight-module`.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 4 week 2
  - ➕ (models/base.py): Improve error handling in the update() method and reorganize the delete() method for better readability
  - ➕ (models/weight.py): Add user_id column to link weight entries to the user
  - ➕ (routes/data.py): Add CRUD routes for glycemia and weight entries with error handling
  - ➕ (services/data_service.py): Add CRUD operations for glycemia and weight entries with validation and error handling
  - ✨ (utils/timelaps.py): Add get_time_range function to return time ranges based on period type
  - 📝 (docs/logbook.md): Update progress for day 4 week 2

### 🧪 QA (tests faits)

- [ ] Tests /glycemia /weight
  - [ ] Tests sur Glycemia
  - [ ] Tests sur Weight

### 💡 Notes / décisions

- Pas de remontées, l'ensemble de la session de travail s'est très bien passé.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Le fait que j'ai des classes très proches en terme de gestion me permet de gagner beaucoup de temps sur l'implémentation de leurs services et de leurs routes.
  - La BaseModel est très pratique par sont héritage de fonctions de base.
- ⚠️ À améliorer :
  - Je penses que je peux optimiser mes fonctions de services pour l'authentification en utilisant les fonctions de base de la BaseModel, mais pour l'instant elles sont fonctionnelles, aussi je les modifierais seulement si j'ai le temps en fin de MVP.

---

## Jour 12 – Activity/Meal services + routes (10/10/25)

### 🎯 Objectifs du jour

- Créer les classes Activity et Meal
- Implémenter les services CRUD pour les classes Activity et Meal
- Implémenter les routes /data/activity et /data/meal

### ✅ Réalisé

- [X] Création classe Activity
- [X] Création classe Meal
- [X] Implémenter services CRUD Activity
- [X] Implémenter routes /data/activity
- [X] Implémenter services CRUD Meal
- [X] Implémenter routes /data/meal

### 🪲 Bugs / difficultés rencontrées

- Pas de difficultés.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des classes Glycemia et Weight → `glycemia-weight-module`. → Branche mergée et supprimée.
  - Mise à jour du journal de bord → `logbook`.
  - Branche tirée pour la gestion des classes Activity et Meal → `activity-meal-module`. → Branche mergée et supprimée.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 5 week 2
  - ✨ (models/activity.py): Add Activity model with validation for description and duration
  - ✨ (models/meal.py): Add Meal model with validation for meal type and description
  - ➕ (services/data_service.py): Add activity and meal management functions, including validation, creation, retrieval, update, and deletion of entries
  - ➕ (routes/data.py): Add activity and meal management routes with CRUD operations and logging
  - ➕ (models/init.py): Import Activity and Meal models in the initialization module
  - ➕ (models/user.py): Add activity and meal relationships to the User model
  - ♻️ (models/glycemia.py): Add info logging for glycemia validation
  - 📝 (docs/logbook.md): Update progress for day 5 week 2

### 🧪 QA (tests faits)

- [ ] Pas de tests pour cette session de travail.

### 💡 Notes / décisions

- Tout s'est bien passé.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Mon architecture porte ses fruits. L'implémentation des classes, services et routes est grandement facilitée.
- ⚠️ À améliorer :
  - Je penses que je pourais améliorer mon fichier de routes qui n'est pas DRY, à voir pour après le MVP.

---

## Jour 13 – Medication/Mood & HealthProfessional/Note classes + services + routes (11/10/25)

### 🎯 Objectifs du jour

- Créer les classes Medication et Mood
- Implémenter les services CRUD pour les classes Medication et Mood
- Implémenter les routes /data/medication et /data/mood
- Créer les classes HealthProfessional et Note
- Implémenter les services CRUD pour les classes HealthProfessional et Note
- Implémenter les routes /data/health_professional et /data/note

### ✅ Réalisé

- [X] Création classe Medication
- [X] Création classe Mood
- [X] Implémenter services CRUD Medication
- [X] Implémenter routes /data/medication
- [X] Implémenter services CRUD Mood
- [X] Implémenter routes /data/mood
- [X] Création classe HealthProfessional
- [X] Création classe Note
- [X] Implémenter services CRUD HealthProfessional
- [X] Implémenter routes /data/health_professional
- [X] Implémenter services CRUD Note
- [X] Implémenter routes /data/note

### 🪲 Bugs / difficultés rencontrées

- Pas de difficultés particulières, juste besoin d'une piqure de rappel sur les relations entre tables (Column, relationship).

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des classes Medication et Mood → `medication-mood-module`. → Branche mergée et supprimée.
  - Branche tirée pour la gestion des classes HealthProfessional et Note → `healthpros-note-module`. → Branche mergée et supprimée.
  - Mise à jour du journal de bord → `logbook`.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 6 week 2
  - ✨ (models/mood.py): Add Mood model with description validation and error handling
  - ✨ (models/medication.py): Add Medication class with attribute validation and error handling
  - ➕ (services/data_service.py): Add Mood and Medication management functions with validation and CRUD operations
  - ➕ (routes/data.py): Add mood and medication management routes with CRUD operations and error handling
  - ➕ (models/user.py): Add relationships for comments, forum posts, health professionals, medications, moods, and notes
  - ➕ (models/init.py): Add imports for Glycemia, Weight, Activity, Meal, Mood, and Medication models
  - ✨ (models/health_professional.py): Add HealthProfessional class with attribute validation for fullname, speciality, and phone
  - ✨ (models/note.py): Add Note class with attribute validation for title and content
  - ➕ (services/data_service.py): Add functions to manage health professionals and associated notes
  - ➕ (routes/data.py): Add routes for managing health professionals and their notes
  - ➕ (models/init.py): Add HealthProfessional and Note to the initialization module
  - ➕ (utils/validators.py): Add regex pattern for phone number validation
  - 📝 (docs/logbook.md): Update progress for day 6 week 2

### 🧪 QA (tests faits)

- [ ] Pas de tests pour cette session de travail.

### 💡 Notes / décisions

- Suivis du planning : Le plus long à faire finalement c'est le contenu de mes classes ensuite pour les services et les routes, c'est sensiblement la même chose.
- Plusieurs fois dans l'élaboration de mes classes, ajouter des attributs était tentant, toutefois je suis restée dans le cadre de mon MVP mais je me les suis notés pour une V2.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - J'ai pus élaborer et finaliser 4 classes en une journée, je rattrape mon retard sur mon planning. Il m'en restera 2 et ensuite les tests avec Pytest et le backend sera terminé, j'ai hâte.
  - Arrivant à la fin de mon backend, je me félicite vraiment d'avoir aussi bien construit mes classes, c'est un gain de temps incroyable, je garderais cette architecture et ce reflexe pour tout mes futur projets perso.
- ⚠️ À améliorer :
  - Si je dois faire un pré-bilan, je dois m'améliorer sur :
    - La gestion des listes/dictionnaires/tuples.
    - Le contenu de mes responses.
    - Le typage de mes fonctions (je veux faire la paix avec Pylance).

---

## Jour 14 – ForumPost/Comment & Article classes + services + routes (12/10/25)

### 🎯 Objectifs du jour

- Créer les classes ForumPost, Comment et Article
- Implémenter les services CRUD pour les classes ForumPost, Comment et Article
- Implémenter les routes /data/forum_post, /data/comment et /data/article

### ✅ Réalisé

- [X] Création classe ForumPost
- [X] Création classe Comment
- [X] Création classe Article
- [X] Implémenter services CRUD ForumPost
- [X] Implémenter routes /data/forum_post
- [X] Implémenter services CRUD Comment
- [X] Implémenter routes /data/comment
- [X] Implémenter services CRUD Article
- [X] Implémenter routes /data/article

### 🪲 Bugs / difficultés rencontrées

- Des difficultés sur la gestion des likes.
- Des difficultés pour utiliser plusieurs tables ensembles dans mes services et routes (ForumPost/Comment)

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour la gestion des classes ForumPost, Comment et Article → `forum-comment-article-module`. → Branche mergée et supprimée.
  - Mise à jour du journal de bord → `logbook`.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 7 week 2
  - ✨ (models/forum_post.py): Add ForumPost class with validation for titles, content, and likes
  - ✨ (models/comment.py): Add Comment class with validation for content and likes
  - ✨ (models/article.py): Add Article class with validation for title, content, and likes
  - ➕ (services/data_service.py): Add forum post and comment management features, including validation, creation, retrieval, update, and deletion
  - ➕ (routes/data.py): Add routes for managing forum posts, comments, and articles, including creation, retrieval, update, and deletion
  - ➕ (models/base.py): Add increment_likes method to manage like counter and improve error handling during deletion
  - ➕ (models/user.py): Add liked_posts, liked_comments, and liked_articles relationships to manage user interactions with posts, comments, and articles
  - ➕ (models/init.py): Add tables to manage user likes on posts, comments, and articles
  - ➕ (utils/validators.py): Rename function for user field validation, create text field validation function, and add regex patterns
  - 📝 (docs/logbook.md): Update progress for day 7 week 2

### 🧪 QA (tests faits)

- [ ] Pas de tests pour cette session de travail.

### 💡 Notes / décisions

- Déclaration des likes dans le MVP, mais pas de la gestion complète (like/dislike). J'ai décidé d'aller au bout de l'idée, j'ai un peu dépassé mon MVP.
- Backend complet 🎉, mais :
  - Décision 1 : Prendre la première journée de la semaine 3 pour tester l'ensemble du backend et debuguer.
  - Décision 2 : Refactorisation des fichiers data.py (routes) et data_service.py (services), avec relancement des tests après chaque refactorisation.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Le backend est fait !! 🎉
- ⚠️ À améliorer :
  - Structure des fichiers → Refactorisation.

---

## Jour 15 – Tests backend (13/10/25)

### 🎯 Objectifs du jour

- Unitest de l'ensemble du backend Flask
- Refactorisation des fichiers de code
- Vérification que la refactorisation est Ok
- Tests Postman

### ✅ Réalisé

- [X] Création des fichiers des tests Pytest
- [ ] Tests Pytest (en cours)
- [ ] Debugue
- [ ] Refactorisation des fichiers
- [ ] Tests Pytest
- [ ] Tests Postman

### 🪲 Bugs / difficultés rencontrées

- Reprise d'une grande partie de mes fonctions qui utilisent mes success_response et mes error_response.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour les tests unitaire → `test-module`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 1 week 3
  - ✨🧪 (tests/): Implement tests for creating, reading, updating, and deleting medications, including edge cases and role-based access across models, services, and routes
  - 🧪♻️ (models/): Refactor model code based on Pytest results of Activity
  - 🧪♻️ (routes/): Refactor routes code based on Pytest results of Activity
  - 🧪♻️ (services/): Refactor services code based on Pytest results of Activity
  - 📝 (docs/logbook.md): Update progress for day 1 week 3

### 🧪 QA (tests faits)

- [ ] tests Pytest auth
- [ ] tests Pytest user
- [ ] tests Pytest glycemia
- [ ] tests Pytest weight
- [X] tests Pytest activity
- [ ] tests Pytest mood
- [ ] tests Pytest medication
- [ ] tests Pytest meal
- [ ] tests Pytest health_professional
- [ ] tests Pytest note
- [ ] tests Pytest forum_post
- [ ] tests Pytest comment
- [ ] tests Pytest article

- [ ] tests Postman auth
- [ ] tests Postman user
- [ ] tests Postman glycemia
- [ ] tests Postman weight
- [ ] tests Postman activity
- [ ] tests Postman mood
- [ ] tests Postman medication
- [ ] tests Postman meal
- [ ] tests Postman health_professional
- [ ] tests Postman note
- [ ] tests Postman forum_post
- [ ] tests Postman comment
- [ ] tests Postman article

### 💡 Notes / décisions

- NE PLUS JAMAIS FAIRE DE "JOLIES" RESPONSES.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Après avoir expérimenté avec Activity, je sais maintenant où sont mes erreurs, le debugue des autres entités devrait être plus rapide.
  - Les logs me permettent de voir et comprendre les erreurs Pytest: c'était vraiment une bonne idée.
- ⚠️ À améliorer :
  - NE PLUS JAMAIS FAIRE DE "JOLIES" RESPONSES.

---

## Jour 16 – Tests backend (14/10/25)

### 🎯 Objectifs du jour

- Unitest de l'ensemble du backend Flask
- Refactorisation des fichiers de code
- Vérification que la refactorisation est Ok
- Tests Postman

### ✅ Réalisé

- [ ] Tests Pytest (en cours)
- [ ] Debugue (en cours)
- [ ] Refactorisation des fichiers (en cours)
- [ ] Tests Pytest (en cours)
- [ ] Tests Postman

### 🪲 Bugs / difficultés rencontrées

- Pas de difficultés particulières, correction du code selon les résultat du test, en série puisque toutes les fonctions sont sensiblement les mêmes pour chaque entité.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour les tests unitaire → `test-module`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 2 week 3
  - 🧪♻️ (models/glycemia.py): Refactor model code based on Pytest results of Glycemia
  - 🧪♻️ (services/): Refactor services code based on Pytest results of Glycemia
  - 🧪♻️ (routes/): Refactor routes code based on Pytest results of Glycemia
  - 🧪♻️ (tests/): Update user payloads and glycemia tests to reflect new data structure
  - 📝 (docs/logbook.md): Update progress for day 2 week 3

### 🧪 QA (tests faits)

- [ ] tests Pytest auth
- [ ] tests Pytest user
- [X] tests Pytest glycemia
- [ ] tests Pytest weight
- [X] tests Pytest activity
- [ ] tests Pytest mood
- [ ] tests Pytest medication
- [ ] tests Pytest meal
- [ ] tests Pytest health_professional
- [ ] tests Pytest note
- [ ] tests Pytest forum_post
- [ ] tests Pytest comment
- [ ] tests Pytest article

- [ ] tests Postman auth
- [ ] tests Postman user
- [ ] tests Postman glycemia
- [ ] tests Postman weight
- [ ] tests Postman activity
- [ ] tests Postman mood
- [ ] tests Postman medication
- [ ] tests Postman meal
- [ ] tests Postman health_professional
- [ ] tests Postman note
- [ ] tests Postman forum_post
- [ ] tests Postman comment
- [ ] tests Postman article

### 💡 Notes / décisions

- Poursuite des tests unitaires:
  - Décision de faire passer les fichiers de tests un par un.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Prise de recule sur le planning et la quantité de travail → Rendez-vous avec Axel.
  - Quelques correction sur les fonctions par rapport aux tests mais moins que ce que je pensais.
- ⚠️ À améliorer :
  - Etre plus positive.

---

## Jour 17 – Tests backend (15/10/25)

### 🎯 Objectifs du jour

- Unitest de l'ensemble du backend Flask
- Refactorisation des fichiers de code

### ✅ Réalisé

- [ ] Tests Pytest (en cours)
- [ ] Debugue (en cours)

### 🪲 Bugs / difficultés rencontrées

-

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour les tests unitaire → `test-module`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 3 week 3
  - 🧪♻️ (models/weight.py): Refactor model code based on Pytest results of Weight
  - 🧪♻️ (services/): Refactor services code based on Pytest results of Weight, Note, Mood, Medication, Meal, Health_professional
  - 🧪♻️ (routes/): Refactor routes code based on Pytest results of Weight, Note, Mood, Medication, Meal, Health_professional
  - 🧪♻️ (tests/): Update tests to reflect new data structure
  - 📝 (docs/logbook.md): Update progress for day 3 week 3

### 🧪 QA (tests faits)

- [ ] tests Pytest auth
- [ ] tests Pytest user
- [X] tests Pytest glycemia
- [X] tests Pytest weight
- [X] tests Pytest activity
- [X] tests Pytest mood
- [X] tests Pytest medication
- [X] tests Pytest meal
- [X] tests Pytest health_professional
- [X] tests Pytest note
- [ ] tests Pytest forum_post
- [ ] tests Pytest comment
- [ ] tests Pytest article

### 💡 Notes / décisions

- Poursuite des tests.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Mêmes retours que le jour précédent.
- ⚠️ À améliorer :
  - Mêmes retours que le jour précédent.

---

## Jour 18 – Tests backend (16/10/25)

### 🎯 Objectifs du jour

- Unitest de l'ensemble du backend Flask
- Refactorisation des fichiers de code

### ✅ Réalisé

- [X] Tests Pytest (en cours)
- [X] Debugue (en cours)

### 🪲 Bugs / difficultés rencontrées

- Fichiers de tests générés par Copilot, problèmes de cohérence avec les tests générés et l'architecture du projet Sweet. → Perte de temps à la corrections des tests.
- Doutes sur l'authentification par le token avec jwt_required() dans les routes à causes des tests mais après recherches tout va bien, c'est seulement que comme les tests s'enchainent, les token restent en mémoire et créent des faux négatifs.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour les tests unitaire → `test-module`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :
  - 📝 (docs/logbook.md): Set objectives for day 4 week 3
  - 🧪♻️ (tests/): Update tests to reflect new data structure
  - 🧪♻️ (routes/data.py): Refactor forum post and comment routes for clarity and consistency
  - 🧪♻️ (services/data_service.py): Simplify error handling in post updates and validate comments
  - 🧪♻️ (utils/validator.py): Modify character length patterns for forum post field validation
  - 📝 (docs/logbook.md): Update progress for day 4 week 3

### 🧪 QA (tests faits)

- [X] tests Pytest auth
- [X] tests Pytest user
- [X] tests Pytest glycemia
- [X] tests Pytest weight
- [X] tests Pytest activity
- [X] tests Pytest mood
- [X] tests Pytest medication
- [X] tests Pytest meal
- [X] tests Pytest health_professional
- [X] tests Pytest note
- [X] tests Pytest forum_post
- [X] tests Pytest comment
- [X] tests Pytest article

### 💡 Notes / décisions

- Poursuite des tests.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Mêmes retours que le jour précédent.
- ⚠️ À améliorer :
  - Mêmes retours que le jour précédent.

---

## Jour 19 – Refactorisation des routes et services (17/10/25)

### 🎯 Objectifs du jour

- Refactorisation des routes et services.
- Tests Pytest pour sécuriser la refactorisation.

### ✅ Réalisé

- [X] Refactorisation de la route et des services de Activity
- [X] Refactorisation de la route et des services de Article
- [X] Refactorisation de la route et des services de Auth
- [ ] Refactorisation de la route et des services de Comment
- [ ] Refactorisation de la route et des services de Forum_post
- [ ] Refactorisation de la route et des services de Glycemia
- [ ] Refactorisation de la route et des services de Health_pros
- [ ] Refactorisation de la route et des services de Meal
- [ ] Refactorisation de la route et des services de Medication
- [ ] Refactorisation de la route et des services de Mood
- [ ] Refactorisation de la route et des services de Note
- [ ] Refactorisation de la route et des services de User
- [ ] Refactorisation de la route et des services de Weight

### 🪲 Bugs / difficultés rencontrées

- Beaucoup de fonctions à refactoriser, je dois également adapter mes tests pour vérifier que tout se passe bien: Prend du temps.

### 🔀 SCM (branches & commits)

- Branches :
  - Branche tirée pour les tests unitaire → `test-module`.
  - Mise à jour du journal de bord → `logbook`.

- Commits :

  - 📝 (docs/logbook.md): Set objectives for day 5 week 3
  - ♻️ (app/init.py): Refactor app initialization and register additional blueprints for improved structure
  - ➕ (models/base.py): Improve save and update methods with logging messages and attribute validation
  - ♻️ (routes/article_routes.py, services/article_service.py): Refactor Article routes and services by extracting them from data.py and data_service.py to improve code readability and maintainability
  - ♻️ (routes/activity_routes.py, services/activity_service.py): Refactor Activity routes and services by extracting them from data.py and data_service.py to improve code readability and maintainability
  - ♻️ (routes/auth_routes.py, services/auth_service.py): Refactor auth routes and services by extracting them from auth.py and auth_service.py to improve code readability and maintainability
  - ➕ (routes/forum_routes.py, services/forum_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➕ (routes/glycemia_routes.py, services/glycemia_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➕ (routes/meal_routes.py, services/meal_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➕ (routes/medication_routes.py, services/medication_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➕ (routes/mood_routes.py, services/mood_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➕ (routes/note_routes.py, services/note_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➕ (routes/professional_routes.py, services/professional_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➕ (routes/weight_routes.py, services/weight_service.py): Add placeholder files in preparation for refactoring data.py and data_service.py modules
  - ➖ (services/email_service.py): Remove unused file
  - 📝 (docs/logbook.md): Update progress for day 5 week 3

### 🧪 QA (tests faits)

- [ ] Test Pytest Activity
- [ ] Test Pytest Article
- [ ] Test Pytest Auth
- [ ] Test Pytest Comment
- [ ] Test Pytest Forum_post
- [ ] Test Pytest Glycemia
- [ ] Test Pytest Health_pros
- [ ] Test Pytest Meal
- [ ] Test Pytest Medication
- [ ] Test Pytest Mood
- [ ] Test Pytest User
- [ ] Test Pytest Weight
- [ ] Test Pytest Note

### 💡 Notes / décisions

- Pas de remonté, l'opération de refactorisation suit son cours.

### 🔄 Rétro rapide (fin de journée)

- ✅ Points positifs :
  - Pour l'instant la refactorisation des trois premières entités se passe bien, je profite de l'occasion pour traduire mes docstring et responses en anglais.
- ⚠️ À améliorer :
  - Je dois absolument corriger mes fichiers de tests et les refaire passer après chaque factorisation pour la valider, pour éviter de revenir sur les fichiers à la fin.
