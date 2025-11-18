import base64
import os
from jwt import ExpiredSignatureError, InvalidTokenError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, decode_token
from flask_mail import Message
from flask import current_app as app, jsonify, make_response
from app import db, mail
from app.models.user import User
from datetime import timedelta


def validate_user_data(data: dict):
    """Validate and return a valid User instance"""
    try:
        if isinstance(data, User):
            app.logger.warning("[BACK][services/auth_service.py][validate_user_data()] 'data' is already a User instance, skipping revalidation.")
            return data
        raw_password = data.pop("password", None)
        user = User(**data)
        if raw_password:
            user.password_hash = raw_password
        app.logger.info(f"[BACK][services/auth_service.py][validate_register_data] Les valeurs enregistrées pour le nouvel user sont valides")
        return user

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/auth_service.py][validate_register_data] Erreur de validation des champs du nouvel utilisateur: {str(e)}")
        raise

def check_availability(data):
    email = data.get("email")
    username = data.get("username")

    email_exists = User.query.filter_by(_email=email).first() is not None
    username_exists = User.query.filter_by(_username=username).first() is not None

    return {
        "email_available": not email_exists,
        "username_available": not username_exists
    }


def create_user(data: dict):
    """Register a new user account"""
    try:
        user = validate_user_data(data)
        user.save()
        cleaned_user = user.to_dict(exclude=["_password_hash", "_first_login", "_role"])
        app.logger.info(f"[BACK][services/auth_service.py][create_user] Utilisateur créé et enregistré en BDD avec succès : {user.email}")
        return cleaned_user

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][create_user] Erreur lors de la création du nouvel utilisateur: {str(e)}")
        raise


def validate_login_data(data: dict):
    """Validate login fields and prepare authentication data"""
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if not password or (not email and not username):
        app.logger.error("[BACK][services/auth_service.py][validate_login_data] Champs invalides : email/username ou mot de passe manquant")
        raise ValueError("Missing email/username or password")
    app.logger.info("[BACK][services/auth_service.py][validate_login_data()] Champs valides pour la connexion")
    return {"email": email, "username": username, "password": password}


def find_user_by_email_or_username(data: dict) -> User: # type: ignore
    """Retrieve a user by email or username"""
    try:
        email = data.get("email")
        username = data.get("username")
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
        if not user:
            app.logger.error("[BACK][services/auth_service.py][find_user_by_email_or_username()] Aucun utilisateur trouvé")
            raise ValueError("User not found")

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Erreur SQL : {str(e)}")
        raise


def authenticate_user(user: User, password: str):
    """Verify that the provided password matches the stored hash"""
    if not user:
        app.logger.error("[BACK][services/auth_service.py][authenticate_user()] Utilisateur introuvable")
        raise ValueError("User not found")
    if not user.verify_password(password):
        app.logger.error(f"[BACK][services/auth_service.py][authenticate_user()] Mot de passe incorrect")
        raise ValueError("Invalid password")
    app.logger.info(f"[BACK][services/auth_service.py][authenticate_user()] Authentification réussie pour l'utilisateur")
    return True


def generate_tokens(user: User, remember_me=False):
    try:
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
        refresh_token = None
        if remember_me:
            refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(hours=48))

        response_data = {
            "message": "Authentification réussie",
            "user": user.email,
            "remember_me": remember_me
        }
        response = make_response(jsonify(response_data), 200)

        # Durée du cookie = cohérente avec la durée du token
        set_access_cookies(response, access_token, max_age=24*3600)
        if refresh_token:
            set_refresh_cookies(response, refresh_token, max_age=48*3600)

        app.logger.info(f"[BACK][generate_tokens()] Cookies JWT définis avec succès pour {user.email}")
        return response

    except Exception as e:
        app.logger.error(f"[BACK][generate_tokens()] Erreur lors de la génération des tokens : {str(e)}")
        raise



def logout_user():
    """Clear JWT cookies and logout the current user"""
    try:
        response = make_response(jsonify({"message": "Logout successful: JWT cookies cleared"}), 200)
        unset_jwt_cookies(response)
        app.logger.info("[BACK][services/auth_service.py][logout_user()] Déconnexion réussie, cookies JWT supprimés")
        return response

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][logout_user()] Erreur lors du nettoyage des cookies : {str(e)}")
        raise


def validate_reset_request(data: dict):
    """Validate password reset request data"""
    email = data.get("email", "").strip()
    if not email:
        app.logger.error("[BACK][services/auth_service.py][validate_reset_request()] Champs invalides : email manquant")
        raise ValueError("Email is required")
    app.logger.info("[BACK][services/auth_service.py][validate_reset_request()] Email valide pour reset password")
    return email


def find_user_by_email(email: str) -> User:
    """Retrieve a user by email"""
    user = User.query.filter_by(_email=email).first()
    if not user:
        app.logger.error(f"[BACK][services/auth_service.py][find_user_by_email()] Aucun utilisateur trouvé pour {email}")
        return # type: ignore
    app.logger.info(f"[BACK][services/auth_service.py][find_user_by_email()] Utilisateur trouvé : {email}")
    return user


def generate_reset_token(user: User):
    """Generate a short-lived JWT reset token"""
    try:
        # Générer le token temporaire
        reset_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=15))
        app.logger.info(f"[BACK][services/auth_service.py][generate_reset_token()] Reset token généré pour {user.email}")
        # Construire la réponse Flask (make_response indispensable)
        response = make_response(jsonify({"message": "Reset token créé"}), 200)
        # Ajouter le token dans les cookies sécurisés
        set_access_cookies(response, reset_token)
        return response

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][generate_reset_token()] Erreur lors de la génération du reset token : {str(e)}")
        raise


def send_reset_email(user: User, reset_token: str):
    """Send password reset email to the user"""
    try:
        # Construire le lien de réinitialisation
        reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={reset_token}"
        # Contenu du mail
        subject = "Réinitialisation de votre mot de passe - Sweet"
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
        return reset_link

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][send_reset_email()] Erreur d'envoi du mail : {str(e)}")
        raise


def validate_reset_token(token: str):
    """Validate and decode a password reset token"""
    try:
        decoded_token = decode_token(token)
        app.logger.info("[BACK][services/auth_service.py][validate_reset_token()] Token valide")
        return decoded_token

    except ExpiredSignatureError:
        app.logger.error("[BACK][services/auth_service.py][validate_reset_token()] Token expiré")
        raise
    except InvalidTokenError:
        app.logger.error("[BACK][services/auth_service.py][validate_reset_token()] Token invalide")
        raise


def clear_reset_token():
    """Invalidate the reset token after use"""
    try:
        response = make_response(jsonify("Token de réinitialisation invalidé avec succès"))
        unset_jwt_cookies(response)
        app.logger.info("[BACK][services/auth_service.py][clear_reset_token] Reset token invalidé avec succès")
        return response

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][clear_reset_token] Erreur : {str(e)}")
        raise


def update_user_password(user: User, new_password: str):
    """Update the user password and commit to the database"""
    try:
        user.password_hash = new_password
        user.save()
        app.logger.info(f"[BACK][services/auth_service.py][update_user_password()]" f"Mot de passe mis à jour avec succès pour {user.email}")
        return True

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][update_user_password()]" f"Erreur lors de la mise à jour du mot de passe pour {user.email} : {str(e)}")
        raise


def sanitize_user_profile(user: User):
    """Return user profile data without sensitive fields"""
    if not isinstance(user, User):
        app.logger.error("[BACK][services/auth_service.py][sanitize_user_profile()] Le user n'est pas une instance de User")
        return None
    exclude = ["_password_hash", "_first_login", "_profile_picture"]
    cleaned_user = user.to_dict(exclude=exclude)
    cleaned_user["profile_picture"] = user.profile_picture
    app.logger.info(f"[BACK][services/auth_service.py][sanitize_user_profile()] Profil nettoyé avec succès pour {user.email}")
    return cleaned_user


def get_user_from_identity() -> User:
    """Retrieve the current user based on JWT identity"""
    user_id = get_jwt_identity()
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        app.logger.error(f"[BACK][services/auth_service.py][get_user_from_identity()] Aucun utilisateur trouvé pour {user_id}")
        return None # type: ignore
    app.logger.info(f"[BACK][services/auth_service.py][get_user_from_identity()] Utilisateur récupéré avec succès : {user.to_dict()}")
    return user


def update_profile(user: User, data: dict):
    """Update user profile fields and commit changes"""
    try:
        for key, value in data.items():
            if hasattr(user, key) and value not in [None, "", "null"]:
                setattr(user, key, value)
        user.save()
        cleaned_user = sanitize_user_profile(user)
        app.logger.info(f"[BACK][services/auth_service.py][update_profile()] Profil mis à jour avec succès pour {user.email}")
        return cleaned_user

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][update_profile()] Erreur lors de la mise à jour du profil pour {user.email} : {str(e)}")
        raise
