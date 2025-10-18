from flask import current_app as app
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.utils.responses import success_response, error_response
from app.services import auth_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ------------------------------------------------- Route POST : /auth/register
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = auth_service.validate_user_data(data)
    return auth_service.create_user(new_user)  # type:ignore

# ---------------------------------------------------- Route POST : /auth/login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Récupérer l’option "se souvenir de moi"
    remember_me = data.get("remember_me", False)
    # Vérifier la validité des données envoyées
    validation = auth_service.validate_login_data(data)
    if isinstance(validation, tuple):  # En cas d'erreur, la fonction renvoie un tuple (response, code)
        app.logger.error("[BACK][routes/auth.py][login()] Champs invalides : échec de la connexion")
        return validation
    # Trouver l'utilisateur via email ou username
    user = auth_service.find_user_by_email_or_username(data)
    if isinstance(user, tuple):
        app.logger.error("[BACK][routes/auth.py][login()] Utilisateur introuvable : échec de la connexion")
        return user
    # Vérifier le mot de passe
    if not auth_service.authenticate_user(user, data["password"]):
        app.logger.error(f"[BACK][routes/auth.py][login()] Mot de passe incorrect pour {user}")
        return error_response("BACK", "routes/auth.py", "login()", "Mot de passe incorrect", 401)
    # Vérifier si c'est la première connexion
    if user.first_login: # type: ignore
        user.first_login = False # type: ignore
        db.session.commit()
        app.logger.info(f"[BACK][routes/auth.py][login()] Première connexion détectée pour {user.email}") # type: ignore
    else:
        app.logger.info(f"[BACK][routes/auth.py][login()] Connexion classique pour {user.email}") # type: ignore
    # Générer les tokens (avec gestion du remember_me)
    return auth_service.generate_tokens(user, remember_me)

# --------------------------------------------------- Route POST : /auth/logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    app.logger.info(f"[BACK][routes/auth.py][logout()] Demande de déconnexion reçue")
    return auth_service.logout_user()

# ---------------------------------------------- Route POST & PUT : /auth/reset
@auth_bp.route('/reset', methods=['POST'])
def reset_request():
    data = request.get_json()
    email = auth_service.validate_reset_request(data)
    user = auth_service.find_user_by_email(email)
    reset_token = auth_service.generate_reset_token(user)
    auth_service.send_reset_email(user, reset_token) # type:ignore
    app.logger.info(f"[BACK][routes/auth.py][reset_request()] Lien de réinitialisation généré avec succès")
    return success_response("BACK", "routes/auth.py", "reset_request()", "Lien de réinitialisation généré avec succès (MVP : token renvoyé dans la réponse).", {user, reset_token}, 200)

@auth_bp.route('/reset/<token>', methods=['PUT'])
def reset_confirm(token):
    data = request.get_json()
    decoded_token = auth_service.validate_reset_token(token)
    if not decoded_token:
        return error_response("BACK", "routes/auth.py", "reset_confirm()", "Token invalide ou expiré", 401)
    user = auth_service.find_user_by_email(decoded_token["sub"]) # type: ignore
    if not user:
        return error_response("BACK", "routes/auth.py", "reset_confirm()", "Utilisateur introuvable", 404)
    auth_service.update_user_password(user, data["new_password"])
    auth_service.clear_reset_token()
    app.logger.info(f"[BACK][routes/auth.py][reset_confirm()] Mot de passe mis à jour avec succès.")
    return success_response("BACK", "routes/auth.py", "reset_confirm()", "Mot de passe mis à jour avec succès.", None, 200)

@auth_bp.route('/password', methods=['PUT'])
@jwt_required()
def update_password():
    data = request.get_json()
    current_user = auth_service.get_user_from_identity()
    if not current_user:
        return error_response("BACK", "routes/auth.py", "update_password()", "Utilisateur introuvable pour ce token", None, 404)
    auth_service.update_user_password(current_user, data["new_password"])
    app.logger.info(f"[BACK][routes/auth.py][update_password()] La modification du mdp à été un succès pour {current_user}")
    return success_response("BACK", "routes/auth.py", "update_password()", "La modification du mdp à été un succès", 200)

# --------------------------------------------- Route GET & PUT : /auth/profile
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def show_profile():
    current_user = auth_service.get_user_from_identity()
    app.logger.info(f"[BACK][routes/auth.py][show_profile()] Récupération de {current_user} avec get_user_from_identity() réussi")
    cleaned_user = auth_service.sanitize_user_profile(current_user)
    app.logger.info(f"[BACK][routes/auth.py][show_profile()] Affichage du profil de {current_user} après l'avoir nettoyé réussi")
    return success_response("BACK", "routes/auth.py", "show_profile()", "Affichage du profil utilisateur réussi", cleaned_user, 200)

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    current_user = auth_service.get_user_from_identity()
    response = auth_service.update_profile(current_user, data)
    app.logger.info(f"[BACK][routes/auth.py][update_profile()] J'ai modifié le profile du user {response}")
    return response
