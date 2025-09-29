# ♻️ Petits bouts de code réutilisable

## Sommaire

- Centralisation des logs (modèle)
- Gestion d'erreurs
- Validation simple
- JWT
- DB (commit & rollback)
- Pagination
- Sécurité (hash & check password)
- Tests Pytest basique

---

## 🔹 Logs

### Qu’est-ce que c’est ?

Un système de suivi qui enregistre des messages pendant que l’application tourne (info, warning, error).

### À quoi ça sert ?

- Comprendre ce qui se passe côté backend (succès/échec).
- Déboguer plus vite quand une requête plante.
- Avoir une trace claire pour la soutenance.

### Comment je l’utilise ?

Partout où je veux savoir ce qui se passe sans avoir besoin de print() :

| **Où ?**             | ✅ Info (OK)                                                         | ⚠️ Warning (inhabituel)                                            | ❌ Error (bloquant)                                       |
| -------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------- |
| **Endpoints Flask**  | - Requête reçue<br>- Action réussie (ex: user créé, donnée ajoutée) | - Données valides mais suspectes (ex: glycémie hors plage normale) | - Requête échouée<br>- Paramètres manquants ou invalides |
| **Fonctions métier** | - Calcul terminé (ex: BMI calculé)<br>- Rapport généré              | - Résultat borderline (ex: tendance glycemie proche seuil)         | - Erreur dans le calcul<br>- Fonction qui crash          |
| **Modèles DB**       | - Nouvel objet créé<br>- Relation ajoutée                           | - Donnée incohérente détectée avant save                           | - Contrainte violée (ex: clé unique email)               |
| **Auth / Sécurité**  | - Connexion réussie<br>- Token validé                               | - Tentative suspecte (ex: 5 logins échoués de suite)               | - Token invalide/expiré<br>- Accès interdit              |
| **Gestion erreurs**  | - Requête traitée sans erreur                                       | - Fallback utilisé (ex: valeur par défaut appliquée)               | - Exception levée (KeyError, ValueError, etc.)           |
| **Tests (Pytest)**   | - Test en cours<br>- Étape réussie                                  | - Résultat inattendu mais non bloquant                             | - Test échoué<br>- AssertionError                        |

```python
app.logger.info("[BACK][auth.py][login_user] User logged in successfully") # ✅
app.logger.warning("[BACK][data.py][add_glycemia] Value near critical threshold") # ⚠️
app.logger.error("[DB][models.py][User] Duplicate email error") # ❌
```

---
## 🪄 Fonctions pratiques (succes/error)
Ces fonctions permettrons de standardiser les messages de succes ou d'erreur, afin qu'elles soient précises afin de débuger plus facilement

```python
from flask import jsonify

def success_response(part, file=None, element=None, message="", data=None, status_code=200):
    """
    Crée une réponse JSON uniforme pour un succès.
    """
    response = {
        "status": "success",
        "part": part,
        "file": file or "N/A",
        "element": element or "N/A",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error_response(part, file=None, element=None, message="", status_code=400):
    """
    Crée une réponse JSON uniforme pour une erreur.
    """
    response = {
        "status": "error",
        "part": part,
        "file": file or "N/A",
        "element": element or "N/A",
        "message": message
    }
    return jsonify(response), status_code
```

Voir en-dessous pour l'utilisation ⬇️

## 🔹 Gestion d’erreurs globale

### Qu’est-ce que c’est ?

Un bloc try/except qui attrape les erreurs et renvoie une réponse JSON claire.

### À quoi ça sert ?

- Éviter que l’app plante avec un stacktrace illisible.
- Uniformiser les retours vers le frontend.
- Ajouter un log au passage pour tracer ce qui s’est passé.

### Comment je l’utilise ?

```python
try:
    # logique métier ou DB
    new_item = Glycemia(value=data["value"])
    db.session.add(new_item)
    db.session.commit()
    app.logger.info("[BACK][data.py][add_glycemia] Glycemia add in successfully")
    return success_response("BACK", "data.py", "add_glycemia", "Glycemia added successfully", new_item.to_dict(), 201)

except KeyError as e:
    app.logger.error(f"[BACK][data.py][add_glycemia] Missing field: {str(e)}")
    return error_response("BACK", "data.py", "add_glycemia", f"Missing required field: {str(e)}", 400)

except ValueError as e:
    app.logger.error(f"[BACK][data.py][add_glycemia] Invalid value: {str(e)}")
    return error_response("BACK", "data.py", "add_glycemia", f"Invalid value: {str(e)}", 400)

except Exception as e:
    app.logger.error(f"[BACK][data.py][add_glycemia] Unexpected error: {str(e)}")
    return error_response("BACK", "data.py", "add_glycemia", f"Unexpected error: {str(e)}", 500)
```

## 🔹 Gestion des erreurs DB

### Qu’est-ce que c’est ?

Attraper une erreur SQLAlchemy (ex. contrainte violée) et rollback la session.

### À quoi ça sert ?

- Éviter un blocage de session.
- Donner un retour propre au frontend.

### Comment je l’utilise ?

```python
try:
    db.session.add(obj)
    db.session.commit()
    app.logger.info(f"[DB][{obj.__tablename__}] Commit succes")
    return success_response("DB", None, f"{obj.__tablename__}", "Commit succes", 201)
except Exception as e:
    db.session.rollback()
    app.logger.error(f"[DB][{obj.__tablename__}] Commit failed: {str(e)}")
    return error_response("DB", None, f"{obj.__tablename__}", "Database error", 400)
```

## 🔹 Gestion erreurs Flask (handlers globaux)

### Qu'est ce que c'est ?

Un “catcher” qui intercepte automatiquement certaines erreurs HTTP.
Ils vont me servir comme dernier filet de sécurité pour attrapper les erreurs "surprise" lors des requêtes.

### A quoi ça sert ?

Ne pas répéter try/except partout → un seul endroit central gère certaines erreurs.

### Comment je l'utilise ?

```python
from flask import request

# 400 - Bad Request
@app.errorhandler(400)
def bad_request(e):
    app.logger.error(f"[BACK][ROUTING] Bad request on {request.path} ({request.method}) - {str(e)}")
    return error_response(
        "BACK",
        "routing",
        "N/A",
        f"Bad request on {request.path} ({request.method}) - {str(e)}",
        status_code=400
    )

# 401 - Unauthorized
@app.errorhandler(401)
def unauthorized(e):
    app.logger.warning(f"[BACK][AUTH] Unauthorized access attempt on {request.path}")
    return error_response(
        "BACK",
        "auth",
        "N/A",
        f"Unauthorized access to {request.path}",
        status_code=401
    )

# 403 - Forbidden
@app.errorhandler(403)
def forbidden(e):
    app.logger.warning(f"[BACK][AUTH] Forbidden access attempt on {request.path}")
    return error_response(
        "BACK",
        "auth",
        "N/A",
        f"Forbidden access to {request.path}",
        status_code=403
    )

# 404 - Not Found
@app.errorhandler(404)
def not_found(e):
    app.logger.warning(f"[BACK][ROUTING] Route not found: {request.path} ({request.method})")
    return error_response(
        "BACK",
        "routing",
        "N/A",
        f"Route not found: {request.path} ({request.method})",
        status_code=404
    )

# 500 - Internal Server Error
@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"[BACK][UNKNOWN] Internal server error on {request.path}: {str(e)}")
    return error_response(
        "BACK",
        "unknown",
        "unexpected",
        f"Internal server error: {str(e)}",
        status_code=500
    )
```

## 🔹 Gestion erreurs JWT

### Qu'est ce que c'est ?

Des handlers spéciaux pour les erreurs liées aux tokens JWT.

### A quoi ça sert ?

Donner un retour clair quand le token est invalide ou expiré.

### Comment je l'utilise ?

```python
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    app.logger.error(f"[BACK][auth.py][JWT] Invalid token - Reason: {reason}")
    return error_response("BACK", "auth.py", "JWT", f"Invalid token - Reason: {reason}", 401)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    app.logger.warning(
        f"[BACK][auth.py][JWT] Expired token for user_id={jwt_payload.get('sub')}"
    )
    return error_response("BACK", "auth.py", "JWT", f"Token expired for user_id={jwt_payload.get('sub')}", 401
    )

@jwt.unauthorized_loader
def missing_token_callback(reason):
    app.logger.warning(f"[BACK][auth.py][JWT] Missing token - {reason}")
    return error_response("BACK", "auth.py", "JWT", f"Missing token - {reason}", 401)
```

---

## 🔹 Validations - Super fonctions générique

### ➡️ Validate_text()

#### Qu'est ce que c'est ?

Une fonction qui vérifie qu’un champ texte est propre : pas vide (si obligatoire), pas trop long, sans caractères interdits, et conforme à une regex au besoin (ex: autoriser uniquement lettres/chiffres).

#### À quoi ça sert ?

- Empêcher les injections (< script>, SQL, etc.).
- Vérifier que les champs texte (nom, description, titre, note, contenu forum…) respectent tes règles.

#### Comment je l’utilise ?

1. Fonction :

```python
import re

def validate_text(value, field_name, required=True, max_length=255, regex=r"^[a-zA-Z0-9\s.,!?'-]+$"):
    """
    Valide un champ texte.
    - required : False si le champ peut être vide
    - max_length : longueur max autorisée
    - regex : pattern autorisé (par défaut lettres, chiffres, ponctuation simple)
    """
    if required and (value is None or str(value).strip() == ""):
        raise ValueError(f"{field_name} is required")

    if value and len(str(value)) > max_length:
        raise ValueError(f"{field_name} must be <= {max_length} characters")

    if value and regex and not re.match(regex, str(value)):
        raise ValueError(f"{field_name} contains invalid characters")

    return str(value).strip() if value else None
```

2. Utilisation :

```python
title = validate_text(data.get("title"), "Forum title", max_length=100)
content = validate_text(data.get("content"), "Forum content", max_length=1000)
```

3. Où ?

Sur pratiquement tout les champs de formulaire

### ➡️ validate_range()

#### Qu’est-ce que c’est ?

Une fonction qui vérifie qu’une valeur numérique est bien dans une plage définie (min–max).

#### À quoi ça sert ?

- Vérifier les données santé : glycémie, poids, activité (durée), humeur, dose, stock.
- Éviter les valeurs absurdes (glycémie à -10, poids à 900, humeur à 42).

#### Comment je l’utilise ?

1. fonction:

```python
def validate_range(value, field_name, min_val=None, max_val=None, type_=int):
    """
    Valide qu'une valeur numérique est bien dans la plage [min_val, max_val].
    - type_ : int ou float
    """
    if value is None:
        raise ValueError(f"{field_name} is required")

    try:
        value = type_(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a {type_.__name__}")

    if min_val is not None and value < min_val:
        raise ValueError(f"{field_name} must be >= {min_val}")

    if max_val is not None and value > max_val:
        raise ValueError(f"{field_name} must be <= {max_val}")

    return value
```
2. Utilisation

```python
glycemia_value = validate_range(data.get("value"), "Glycemia", min_val=20, max_val=600)
weight_value = validate_range(data.get("weight"), "Weight", min_val=30, max_val=300, type_=float)
mood_score = validate_range(data.get("score"), "Mood", min_val=1, max_val=5)
```

3. Où ?

Au moins sur toutes les données de santé : glycémie, poids, activité, ...

## 🔹 Validations spécialisées

### ➡️ validate_email()

#### Qu’est-ce que c’est ?

Une fonction qui vérifie que l’email respecte un format standard.

#### À quoi ça sert ?

- Empêcher qu’un utilisateur s’inscrive avec un email invalide.
- Éviter des doublons farfelus dans la DB.

#### Comment je l’utilise ?

```python
import re

def validate_email(email):
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not email or not re.match(regex, email):
        raise ValueError("Invalid email format")
    return email.lower()
```

Utilisation :

```python
email = validate_email(data.get("email"))
```

### ➡️ validate_password()

##### Qu’est-ce que c’est ?

Une fonction qui vérifie la robustesse d’un mot de passe.

#### À quoi ça sert ?

- Forcer des règles minimales de sécurité.
- Prévenir les mdp trop faibles (123456, azerty).

#### Comment je l’utilise ?

```python
def validate_password(password):
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one number")
    return password
```

Utilisation :

```python
password = validate_password(data.get("password"))
```

### ➡️ validate_choice()

#### Qu’est-ce que c’est ?

Une fonction qui vérifie qu’une valeur appartient à une liste prédéfinie.

#### À quoi ça sert ?

- Limiter les rôles utilisateur (user, admin).
- Limiter les types d’activité (ex: walking, running, cycling).

#### Comment je l’utilise ?

```python
def validate_choice(value, field_name, allowed_values):
    if value not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}")
    return value
```

Utilisation :

```python
role = validate_choice(data.get("role"), "Role", ["user", "admin"])
activity = validate_choice(data.get("type"), "Activity type", ["walking", "running", "cycling"])
```

---

## 🔹 JWT

### Configuration JWT

#### Qu’est-ce que c’est ?

La configuration globale des tokens JWT dans Flask.

#### À quoi ça sert ?

- Définir les durées de vie de tes tokens.
- Centraliser la clé secrète.

#### Comment je l’utilise ?

```python
from datetime import timedelta

app.config["JWT_SECRET_KEY"] = "super-secret-key"  # ⚠️ mettre dans .env
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  # 24h
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=3)   # 3 jours
```

### Génération conditionnelle des tokens

#### Qu’est-ce que c’est ?

Une fonction qui crée un access token pour tout le monde et un refresh token seulement si « se souvenir de moi » est coché.

#### À quoi ça sert ?

- Respecter les choix de l’utilisateur.
- Éviter d’avoir des refresh tokens inutiles.

#### Comment je l’utilise ?

```python
from flask_jwt_extended import create_access_token, create_refresh_token

def generate_tokens(user, remember_me=False):
    """
    Génère un access token (24h) et éventuellement un refresh token (3 jours)
    """
    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    refresh_token = None
    if remember_me:  # seulement si "se souvenir de moi" est coché
        refresh_token = create_refresh_token(identity=user.id)

    return access_token, refresh_token
```

➡️ Exemple dans la route login :

```python
remember_me = data.get("remember_me", False)
access, refresh = generate_tokens(user, remember_me)

payload = {"access": access}
if refresh:
    payload["refresh"] = refresh

return success_response("BACK", "auth.py", "login", "Login successful", payload)
```

### Vérification d’accès par rôle

#### Qu’est-ce que c’est ?

Un décorateur pour restreindre l’accès à certaines routes (admin only).

#### À quoi ça sert ?

- Centraliser la logique des rôles.
- Éviter de dupliquer des if role != "admin" dans toutes les routes.

#### Comment je l’utilise ?

```python
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != required_role:
                return error_response("BACK", "auth.py", "role_required", f"Access denied: {required_role} only", 403)
            return fn(*args, **kwargs)
        return decorated
    return wrapper
```

➡️ Exemple :

```python
@app.route("/articles", methods=["POST"])
@role_required("admin")
def create_article():
    ...
```

### Récupération de l’utilisateur courant

#### Qu’est-ce que c’est ?

Un helper pour obtenir l’objet User depuis le JWT.

#### À quoi ça sert ?

- Éviter de répéter la logique get_jwt_identity() + User.query.get() partout.

#### Comment je l’utilise ?

```python
from flask_jwt_extended import get_jwt_identity
from models import User

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)
```

➡️ Exemple :

```python
@app.route("/data/glycemia", methods=["POST"])
def add_glycemia():
    user = get_current_user()
    ...
```

### Refresh token route

#### Qu’est-ce que c’est ?

Une route qui génère un nouvel access token à partir d’un refresh token valide.

#### À quoi ça sert ?

- Permettre à l’utilisateur de rester connecté sans re-login.
- Ne fonctionne que si “se souvenir de moi” était activé.

#### Comment je l’utilise ?

```python
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

@app.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return success_response("BACK", "auth.py", "refresh", "New access token issued", {"access": access_token})
```

---
