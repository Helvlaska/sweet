from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from app.utils.responses import success_response, error_response
from flask import current_app as app
from sqlalchemy.exc import IntegrityError
from app import db
from datetime import timedelta

# ----------------------------------------------------- Fonctions réutilisables
def validate_user_data(data):
    """Vérifie que les données d'inscription sont présentes et valides (email, password, etc.)."""
    try:
        new_user = User(**data)
        app.logger.error(f"[BACK][services/auth_service.py][validate_register_data()] Les valeurs enregistrées pour le nouvel user sont valides")
        return success_response("BACK", "services/auth_service.py", "validate_register_data()", "Les valeurs enregistrées pour le nouvel user sont valides", new_user.to_dict(), 201)
    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/auth_service.py][validate_register_data()] Invalid value: {str(e)}")
        return error_response("BACK", "services/auth_service.py", "validate_register_data()", f"Invalid value: {str(e)}", 400)

# ------------------------------------------------------------------- /Register
def create_user(new_user):
    """Sauvegarde un nouvel utilisateur en base de données après hash du mot de passe.
    Retourne l'utilisateur créé."""
    try:
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"[BACK][services/auth_service.py][create_user()] Utilisateur créé avec succès : {new_user.email}")
        return success_response("BACK", "services/auth_service.py", "create_user()", "Utilisateur créé avec succès", new_user.to_dict(), 201)

    except IntegrityError as e:
        db.session.rollback()
        app.logger.error(f"[BACK][services/auth_service.py][create_user()] Email déjà utilisé : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "create_user()", "Cet email est déjà utilisé", 400)

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[BACK][services/auth_service.py][create_user()] Erreur lors de la création : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "create_user()", f"Erreur interne : {str(e)}", 500)

# ---------------------------------------------------------------------- /Login
def validate_login_data(data):
    """Vérifie que les données de connexion sont présentes (email/username et password)."""
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if not password or (not email and not username):
        app.logger.error("[BACK][services/auth_service.py][validate_login_data()] Champs invalides : email/username ou mot de passe manquant")
        return error_response("BACK", "services/auth_service.py", "validate_login_data()", "Champs invalides : email/username ou mot de passe manquant", 400)
    app.logger.info("[BACK][services/auth_service.py][validate_login_data()] Champs valides pour la connexion")
    return success_response("BACK", "services/auth_service.py", "validate_login_data()", "Champs valides pour la connexion", {"email": email, "username": username, "password": password}, 201)

def find_user_by_email_or_username(data):
    """Retourne un utilisateur à partir de son email ou de son username."""
    email = data.get("email")
    username = data.get("username")
    user = None
    if email:
        user = db.session.query(User).filter_by(_email=email).first()
        if user:
            app.logger.info(f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Utilisateur trouvé par email : {email}")
            return success_response("BACK", "services/auth_service.py", "find_user_by_email_or_username()", "Utilisateur trouvé par email : ", {email}, 201)
    if username:
        user = db.session.query(User).filter_by(_username=username).first()
        if user:
            app.logger.info(f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Utilisateur trouvé par username : {username}")
            return success_response("BACK", "services/auth_service.py", "find_user_by_email_or_username()", "Utilisateur trouvé par username : ", {username}, 201)
    app.logger.error("[BACK][services/auth_service.py][find_user_by_email_or_username()] Aucun utilisateur trouvé")
    return error_response("BACK", "services/auth_service.py", "find_user_by_email_or_username()", "Aucun utilisateur trouvé avec cet email/username", 404)

def authenticate_user(user, password):
    """Vérifie si le mot de passe fourni correspond au hash stocké pour cet utilisateur."""
    if not user:
        app.logger.error("[BACK][services/auth_service.py][authenticate_user()] Utilisateur introuvable")
        return error_response("BACK", "services/auth_service.py", "authenticate_user()", "Utilisateur introuvable", 404)
    if not user.verify_password(password):
        app.logger.error(f"[BACK][services/auth_service.py][authenticate_user()] Mot de passe incorrect")
        return error_response("BACK", "services/auth_service.py", "authenticate_user()", "Mot de passe incorrect", 401)
    app.logger.info(f"[BACK][services/auth_service.py][authenticate_user()] Authentification réussie pour l'utilisateur")
    return success_response("BACK", "services/auth_service.py", "authenticate_user()", "Authentification réussie pour l'utilisateur", {user}, 200)

def generate_tokens(user):
    """Génère et retourne un access_token et un refresh_token pour un utilisateur."""
    try:
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))

        app.logger.info(f"[BACK][services/auth_service.py][generate_tokens()] Tokens générés avec succès pour {user.to_dict()}")
        response = success_response("BACK", "services/auth_service.py", "generate_tokens()", "Tokens générés avec succès pour : ", {user.to_dict(), access_token}, 200)

        #set_access_cookies(response, access_token)

        #if remember_me:
        #    refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(hours=48))
        #    set_refresh_cookies(response, refresh_token)

        #app.logger.info(f"[BACK][services/auth_service.py][generate_tokens()] Tokens générés pour {user.email} (remember_me={remember_me})")
        #return response, 200

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][generate_tokens()] Erreur lors de la génération des tokens : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "generate_tokens()", "Impossible de générer les tokens", 500)


# ---------------------------------------------------------------------- Logout

def logout_user(response):
    """Nettoie les cookies JWT et invalide la session de l'utilisateur."""
    pass


# -------------------------------------------------------------- Reset Password

def validate_reset_request(data):
    """Vérifie que l'email est fourni pour une demande de reset password."""
    pass

def find_user_by_email(email):
    """Retourne un utilisateur à partir de son email, ou None si inexistant."""
    pass

def generate_reset_token(user):
    """Génère un token temporaire de reset pour l'utilisateur (UUID ou JWT avec expiration)."""
    pass

def validate_reset_token(token):
    """Vérifie si le token de reset est valide et non expiré."""
    pass

def invalidate_reset_token(token):
    """Invalide un token de reset après usage pour éviter toute réutilisation."""
    pass

def update_user_password(user, new_password):
    """Met à jour le mot de passe d’un utilisateur (hashé) dans la DB."""
    pass


# ------------------------------------------------------------- Update Password

def validate_new_password(new_password):
    """Vérifie que le nouveau mot de passe est conforme (force, regex, longueur)."""
    pass

def change_password(user, old_password, new_password):
    """Vérifie l'ancien mot de passe puis met à jour avec le nouveau (hashé)."""
    pass


# ----------------------------------------------------------- Gestion du Profil

def get_user_from_identity(identity):
    """Récupère un utilisateur en fonction de l'identité contenue dans le JWT."""
    pass

def sanitize_user_profile(user):
    """Retourne un profil utilisateur nettoyé (sans champs sensibles)."""
    pass

def validate_profile_update(data):
    """Vérifie que les données de mise à jour de profil sont valides (regex, unicité email)."""
    pass

def update_profile(user, data):
    """Met à jour les informations du profil utilisateur en DB avec les données valides."""
    pass
