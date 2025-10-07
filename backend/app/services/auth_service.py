import os
from jwt import ExpiredSignatureError, InvalidTokenError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, decode_token
from flask_mail import Message
from flask import current_app as app, make_response
from sqlalchemy.exc import IntegrityError
from app import db, mail
from app.utils.responses import success_response, error_response
from app.models.user import User
from app.utils.validators import is_valid, EMAIL_PATTERN, PASSWORD_PATTERN
from datetime import timedelta

# ----------------------------------------------------- Fonctions réutilisables
def validate_user_data(data):
    """Vérifie que les données d'inscription sont présentes et valides (email, password, etc.)."""
    try:
        raw_password = data.pop("password", None)
        user = User(**data)
        if raw_password:
            user.password_hash = raw_password
        app.logger.info(f"[BACK][services/auth_service.py][validate_register_data()] Les valeurs enregistrées pour le nouvel user sont valides")
        return user
    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/auth_service.py][validate_register_data()] Invalid value: {str(e)}")
        raise

# ------------------------------------------------------------------- /Register
def create_user(new_user):
    """Sauvegarde un nouvel utilisateur en base de données après hash du mot de passe.
    Retourne l'utilisateur créé."""
    try:
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"[BACK][services/auth_service.py][create_user()] Utilisateur créé avec succès : {new_user.email}")
        cleaned_user = new_user.to_dict(exclude=["_password_hash", "_first_login", "_role"])
        return success_response("BACK", "services/auth_service.py", "create_user()", "Utilisateur créé avec succès", cleaned_user, 201)
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
    return {"email": email, "username": username, "password": password}

def find_user_by_email_or_username(data):
    """Retourne un utilisateur à partir de son email ou de son username."""
    email = data.get("email")
    username = data.get("username")
    try:
        user = None
        if email:
            user = db.session.query(User).filter_by(_email=email).first()
            if user:
                app.logger.info(f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Utilisateur trouvé par email : {email}")
                return user
        if username:
            user = db.session.query(User).filter_by(_username=username).first()
            if user:
                app.logger.info(f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Utilisateur trouvé par username : {username}")
                return user
        app.logger.error("[BACK][services/auth_service.py][find_user_by_email_or_username()] Aucun utilisateur trouvé")
        return None
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Erreur SQL : {str(e)}")
        raise

def authenticate_user(user, password):
    """Vérifie si le mot de passe fourni correspond au hash stocké pour cet utilisateur."""
    if not user:
        app.logger.error("[BACK][services/auth_service.py][authenticate_user()] Utilisateur introuvable")
        return error_response("BACK", "services/auth_service.py", "authenticate_user()", "Utilisateur introuvable", False, 404)
    if not user.verify_password(password):
        app.logger.error(f"[BACK][services/auth_service.py][authenticate_user()] Mot de passe incorrect")
        return error_response("BACK", "services/auth_service.py", "authenticate_user()", "Mot de passe incorrect", False, 401)
    app.logger.info(f"[BACK][services/auth_service.py][authenticate_user()] Authentification réussie pour l'utilisateur")
    return success_response("BACK", "services/auth_service.py", "authenticate_user()", "Authentification réussie pour l'utilisateur", True, 200)

def generate_tokens(user, remember_me=False):
    """Génère et retourne un access_token et un refresh_token pour un utilisateur."""
    try:
        # Générer l'access token de base
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
        app.logger.info(f"[BACK][services/auth_service.py][generate_tokens()] Access token généré pour {user.to_dict()}")
        # Générer le refresh token seulement si "remember me" est activé
        refresh_token = None
        if remember_me:
            refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(hours=48))
            app.logger.info(f"[BACK][services/auth_service.py][generate_tokens()] Refresh token généré (remember_me=True)")
        # Construire la réponse
        response_data = {
            "message": "Authentification réussie",
            "user": user.email,
            "remember_me": remember_me
        }
        response, status_code = success_response("BACK", "services/auth_service.py", "generate_tokens()", "Authentification réussie, tokens créés", response_data, 200)
        # Ajouter les cookies sécurisés à la réponse
        set_access_cookies(response, access_token) # type: ignore
        if refresh_token:
            set_refresh_cookies(response, refresh_token)
        app.logger.info(f"[BACK][services/auth_service.py][generate_tokens()] Cookies JWT définis avec succès pour {user.to_dict()}")
        return response, status_code
    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][generate_tokens()] Erreur lors de la génération des tokens : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "generate_tokens()", f"Erreur lors de la génération des tokens : {str(e)}", 500)

# ---------------------------------------------------------------------- Logout
def logout_user():
    """Nettoie les cookies JWT et invalide la session de l'utilisateur."""
    try:
        # Pour utiliser unset_jwt_cookies() il faut : contruire la réponse → unset_jwt_cookies modifie la réponse → renvoie de la réponse
        response = make_response(success_response("BACK", "services/auth_service.py", "logout_user()", "Déconnexion réussie : Les cookies JWT ont été supprimés", None, 200))
        unset_jwt_cookies(response)
        app.logger.info(f"[BACK][services/auth_service.py][logout_user()] Déconnexion réussie : Les cookies JWT ont été supprimés")
        return response
    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][logout_user()] Erreur lors du nettoyage des cookies : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "logout_user()", f"Erreur lors du nettoyage des cookies : {str(e)}", 500)

# -------------------------------------------------------------- Reset Password
def validate_reset_request(data):
    """Vérifie que l'email est fourni pour une demande de reset password."""
    email = data.get("email", "").strip()
    if not email:
        app.logger.error("[BACK][services/auth_service.py][validate_reset_request()] Champs invalides : email manquant")
        return error_response("BACK", "services/auth_service.py", "validate_reset_request()", "Champs invalides : email manquant", 400)
    if not is_valid(email, EMAIL_PATTERN):
        app.logger.error("[BACK][services/auth_service.py][validate_reset_request()] Format d'email invalide")
        return error_response("BACK", "services/auth_service.py", "validate_reset_request()", "Format d'email invalide", 400)
    app.logger.info("[BACK][services/auth_service.py][validate_reset_request()] Email valide pour reset password")
    return success_response("BACK", "services/auth_service.py", "validate_reset_request()", "Email valide pour reset password", email, 201)

def find_user_by_email(email):
    """Retourne un utilisateur à partir de son email, ou None si inexistant."""
    user = User.query.filter_by(_email=email).first()
    if not user:
        app.logger.error(f"[BACK][services/auth_service.py][find_user_by_email()] Aucun utilisateur trouvé pour {email}")
        return error_response("BACK", "services/auth_service.py", "find_user_by_email()", f"Aucun utilisateur trouvé pour {email}", 404)
    app.logger.info(f"[BACK][services/auth_service.py][find_user_by_email()] Utilisateur trouvé : {email}")
    return success_response("BACK", "services/auth_service.py", "find_user_by_email()", f"Utilisateur trouvé : {email}", user, 201)

def generate_reset_token(user):
    """Génère un token temporaire de reset pour l'utilisateur (UUID ou JWT avec expiration)."""
    try:
        # Générer le token temporaire
        reset_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=15))
        app.logger.info(f"[BACK][services/auth_service.py][generate_reset_token()] Reset token généré pour {user.email}")
        # Construire la réponse Flask (make_response indispensable)
        response = make_response(
            success_response("BACK", "services/auth_service.py", "generate_reset_token()", "Reset token créé", {"user": user.email}, 200)
        )
        # Ajouter le token dans les cookies sécurisés
        set_access_cookies(response, reset_token)
        return response
    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][generate_reset_token()] Erreur lors de la génération du reset token : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "generate_reset_token()", f"Erreur lors de la génération du reset token : {str(e)}", 500)

def send_reset_email(user, reset_token):
    """Envoie un email de réinitialisation du mot de passe via Flask-Mail."""
    try:
        # Construire le lien de réinitialisation
        reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={reset_token}"
        # Contenu du mail
        subject = "🔐 Réinitialisation de votre mot de passe - Sweet"
        html_body = f"""
        <html>
            <body>
                <p>Bonjour {user.first_name},</p>
                <p>Vous avez demandé la réinitialisation de votre mot de passe sur <strong>Sweet</strong>.</p>
                <p>Cliquez sur le lien ci-dessous pour le réinitialiser :</p>
                <p><a href="{reset_link}" target="_blank">{reset_link}</a></p>
                <p>Ce lien expirera dans 15 minutes.</p>
                <p>Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.</p>
                <br>
                <p>L'équipe Sweet 🍃</p>
            </body>
        </html>
        """
        # Création du message
        msg = Message(subject=subject, recipients=[user.email], html=html_body)
        # Envoi du mail
        mail.send(msg)
        app.logger.info(f"[BACK][services/auth_service.py][send_reset_email()] Email envoyé avec succès à {user.email}")
        return success_response("BACK", "services/auth_service.py", "send_reset_email()", f"Email de réinitialisation envoyé à {user.email}", {"reset_link": reset_link}, 200)
    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][send_reset_email()] Erreur d'envoi du mail : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "send_reset_email()", f"Erreur d'envoi du mail : {str(e)}", 500)

def validate_reset_token(token):
    """Vérifie si le token de reset est valide et non expiré."""
    try:
        decoded_token = decode_token(token)
        app.logger.info("[BACK][services/auth_service.py][validate_reset_token()] Token valide")
        return decoded_token
    except ExpiredSignatureError:
        app.logger.error("[BACK][services/auth_service.py][validate_reset_token()] Token expiré")
        return error_response("BACK", "services/auth_service.py", "validate_reset_token()", "Token expiré", 401)
    except InvalidTokenError:
        app.logger.error("[BACK][services/auth_service.py][validate_reset_token()] Token invalide")
        return error_response("BACK", "services/auth_service.py", "validate_reset_token()", "Token invalide", 400)

def invalidate_reset_token(token):
    """Invalide un token de reset après usage pour éviter toute réutilisation."""
    try:
        response = make_response(success_response("BACK", "services/auth_service.py", "invalidate_reset_token()", "Token de réinitialisation invalidé avec succès"))
        unset_jwt_cookies(response)
        app.logger.info("[BACK][services/auth_service.py][invalidate_reset_token()] Reset token invalidé avec succès")
        return response
    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][invalidate_reset_token()] Erreur : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "invalidate_reset_token()", f"Erreur lors de l'invalidation du reset token : {str(e)}", 500)

def update_user_password(user, new_password):
    """Met à jour le mot de passe d’un utilisateur (hashé) dans la DB."""
    try:
        user.password_hash = new_password
        db.session.commit()
        app.logger.info(f"[BACK][services/auth_service.py][update_user_password()]" f"Mot de passe mis à jour avec succès pour {user.email}")
        return success_response("BACK", "services/auth_service.py", "update_user_password()", f"Mot de passe mis à jour avec succès pour {user.email}", None, 200)
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[BACK][services/auth_service.py][update_user_password()]" f"Erreur lors de la mise à jour du mot de passe pour {user.email} : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "update_user_password()", f"Erreur lors de la mise à jour du mot de passe pour {user.email} : {str(e)}", 500)

# ----------------------------------------------------------- Gestion du Profil
def sanitize_user_profile(user):
    """Retourne un profil utilisateur nettoyé (sans champs sensibles)."""
    if not isinstance(user, User):
        app.logger.error("[BACK][services/auth_service.py][sanitize_user_profile()] Le user n'est pas une instance de User")
        return None
    exclude = ["_password_hash", "_role", "_first_login"]
    cleaned_user = user.to_dict(exclude=exclude)
    app.logger.info(f"[BACK][services/auth_service.py][sanitize_user_profile()] Profil nettoyé avec succès pour {user.email}")
    return cleaned_user

def get_user_from_identity():
    """Récupère un utilisateur en fonction de l'identité contenue dans le JWT."""
    user_id = get_jwt_identity()
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        app.logger.error(f"[BACK][services/auth_service.py][get_user_from_identity()] Aucun utilisateur trouvé pour {user_id}")
        return None
    app.logger.info(f"[BACK][services/auth_service.py][get_user_from_identity()] Utilisateur récupéré avec succès : {user.to_dict()}")
    return user

def update_profile(user, data):
    """Met à jour les informations du profil utilisateur en DB avec les données valides."""
    try:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        cleaned_user = sanitize_user_profile(user)
        app.logger.info(f"[BACK][services/auth_service.py][update_profile()] Profil mis à jour avec succès pour {cleaned_user}")
        return success_response("BACK", "services/auth_service.py", "update_profile()", "Profil mis à jour avec succès", cleaned_user, 200)
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[BACK][services/auth_service.py][update_profile()] Erreur lors de la mise à jour du profil pour {user.email} : {str(e)}")
        return error_response("BACK", "services/auth_service.py", "update_profile()", f"Erreur lors de la mise à jour du profil pour {user.email} : {str(e)}", 500)


