"""
[BACK][services/auth_service.py]

Service layer — authentication and user management business logic.
Called exclusively from auth_routes.py.

Exposed functions:
  validate_user_data(data)
  check_availability(data)
  create_user(data)
  complete_first_login(user_id)
  validate_login_data(data)
  find_user_by_email_or_username(data)
  authenticate_user(user, password)
  generate_tokens(user, remember_me)
  logout_user()
  validate_reset_request(data)
  find_user_by_email(email)
  generate_reset_token(user)
  send_reset_email(user, reset_token)
  validate_reset_token(token)
  clear_reset_token()
  update_user_password(user, new_password)
  sanitize_user_profile(user)
  get_user_from_identity()
  update_profile(user, data)
"""


from jwt import ExpiredSignatureError, InvalidTokenError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, decode_token
from flask_mail import Message
from flask import current_app as app, jsonify, make_response
from app import db, mail
from app.models.user import User
from datetime import timedelta
import os


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
    """Check in database if email & username are available"""
    email = data.get("email")
    username = data.get("username")

    response = {}

    if email is not None:
        email_exists = User.query.filter_by(_email=email).first() is not None
        response["email_available"] = not email_exists

    if username is not None:
        username_exists = User.query.filter_by(_username=username).first() is not None
        response["username_available"] = not username_exists

    return response


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


def complete_first_login(user_id: str):
    """
    Marque l'onboarding comme terminé pour l'utilisateur.
    """
    user = User.query.filter_by(id=user_id).first()

    if not user:
        app.logger.error(f"[BACK][services/auth_service.py][complete_first_login] Utilisateur introuvable : {user_id}")
        raise ValueError("Utilisateur introuvable")

    if not user.first_login:
        app.logger.info(f"[BACK][services/auth_service.py][complete_first_login] first_login déjà à False pour {user_id}")
        return user

    user.first_login = False
    user.save()

    app.logger.info(f"[BACK][services/auth_service.py][complete_first_login] Onboarding complété pour {user_id}")
    return user


def validate_login_data(data: dict):
    """Validate login fields and prepare authentication data"""
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not password or (not email and not username):
        app.logger.error(
            "[BACK][services/auth_service.py][validate_login_data] Champs invalides : email/username ou mot de passe manquant"
        )
        raise ValueError("Missing email/username or password")

    app.logger.info("[BACK][services/auth_service.py][validate_login_data()] Champs valides pour la connexion")
    return {"email": email, "username": username, "password": password}


def find_user_by_email_or_username(data: dict) -> User: # type: ignore
    """Retrieve a user by email or username. Raises ValueError if no match is found."""
    try:
        email = data.get("email")
        username = data.get("username")
        user = None

        if email:
            user = db.session.query(User).filter_by(_email=email).first()
            if user:
                app.logger.info(
                    f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Utilisateur trouvé par email : {email}"
                )
                return user

        if username:
            user = db.session.query(User).filter_by(_username=username).first()
            if user:
                app.logger.info(
                    f"[BACK][services/auth_service.py][find_user_by_email_or_username()] Utilisateur trouvé par username : {username}"
                )
                return user

        if not user:
            app.logger.error(
                "[BACK][services/auth_service.py][find_user_by_email_or_username()] Aucun utilisateur trouvé"
            )
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
    """Generate JWT access and optional refresh token, set them as HTTP-only cookies."""
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
    """Retrieve a user by email. Returns None silently if not found — intentional for reset flow (anti-enumeration)."""
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
        return reset_token

    except Exception as e:
        app.logger.error(f"[BACK][services/auth_service.py][generate_reset_token()] Erreur lors de la génération du reset token : {str(e)}")
        raise


def send_reset_email(user: User, reset_token: str):
    """Send password reset email to the user"""
    try:
        # Construire le lien de réinitialisation
        reset_link = f"{os.getenv('FRONTEND_URL')}/forgot-password/{reset_token}"
        # Contenu du mail
        subject = "Réinitialisation de votre mot de passe - Sweet"
        html_body = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Réinitialisation de mot de passe</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 40px 20px;">
                        <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="padding: 40px 40px 30px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">Sweet</h1>
                                </td>
                            </tr>

                            <!-- Content -->
                            <tr>
                                <td style="padding: 40px;">
                                    <h2 style="margin: 0 0 20px; color: #333333; font-size: 24px; font-weight: 600;">
                                        Bonjour {user.first_name} 👋
                                    </h2>

                                    <p style="margin: 0 0 20px; color: #555555; font-size: 16px; line-height: 1.6;">
                                        Vous avez demandé la réinitialisation de votre mot de passe sur <strong>Sweet</strong>.
                                    </p>

                                    <p style="margin: 0 0 30px; color: #555555; font-size: 16px; line-height: 1.6;">
                                        Cliquez sur le bouton ci-dessous pour créer un nouveau mot de passe :
                                    </p>

                                    <!-- Button -->
                                    <table role="presentation" style="margin: 0 auto;">
                                        <tr>
                                            <td style="border-radius: 6px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                                                <a href="{reset_link}" target="_blank" style="display: inline-block; padding: 16px 40px; font-size: 16px; color: #ffffff; text-decoration: none; font-weight: 600; letter-spacing: 0.5px;">
                                                    Réinitialiser mon mot de passe
                                                </a>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Info Box -->
                                    <div style="margin: 30px 0; padding: 16px; background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                                        <p style="margin: 0; color: #856404; font-size: 14px; line-height: 1.5;">
                                            ⏱️ <strong>Important :</strong> Ce lien expirera dans <strong>15 minutes</strong>.
                                        </p>
                                    </div>

                                    <p style="margin: 0 0 10px; color: #777777; font-size: 14px; line-height: 1.6;">
                                        Si le bouton ne fonctionne pas, copiez et collez ce lien dans votre navigateur :
                                    </p>

                                    <p style="margin: 0 0 30px; padding: 12px; background-color: #f8f9fa; border-radius: 4px; word-break: break-all;">
                                        <a href="{reset_link}" target="_blank" style="color: #667eea; text-decoration: none; font-size: 13px;">
                                            {reset_link}
                                        </a>
                                    </p>

                                    <div style="padding: 20px; background-color: #f8f9fa; border-radius: 4px;">
                                        <p style="margin: 0; color: #666666; font-size: 14px; line-height: 1.6;">
                                            🔒 Si vous n'êtes pas à l'origine de cette demande, ignorez cet email. Votre mot de passe restera inchangé.
                                        </p>
                                    </div>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="padding: 30px 40px; background-color: #f8f9fa; border-radius: 0 0 8px 8px; text-align: center;">
                                    <p style="margin: 0 0 10px; color: #333333; font-size: 16px; font-weight: 600;">
                                        L'équipe Sweet
                                    </p>
                                    <p style="margin: 0; color: #999999; font-size: 12px;">
                                        © 2025 Sweet. Tous droits réservés.
                                    </p>
                                </td>
                            </tr>
                        </table>

                        <!-- Bottom Text -->
                        <table role="presentation" style="max-width: 600px; margin: 20px auto 0;">
                            <tr>
                                <td style="text-align: center;">
                                    <p style="margin: 0; color: #999999; font-size: 12px; line-height: 1.5;">
                                        Cet email a été envoyé automatiquement, merci de ne pas y répondre.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
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
    """Retrieve the current user from JWT identity. Returns None if not found — caller must check before use."""
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
