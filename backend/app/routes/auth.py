from flask import current_app as app
from flask import Blueprint, request
from utils.responses import success_response, error_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from app.services.auth_service import validate_user_data, create_user
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ------------------------------------------------- Route POST : /auth/register
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = validate_user_data(data)
    if isinstance(new_user, User):
        return new_user
    return create_user(new_user)

# ---------------------------------------------------- Route POST : /auth/login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Vérifier si tout les champs # Si tout est Ok → success_response + logger.info sont remplis → sinon error_response
      # app.logger.error(f"[BACK][routes/auth.py][login()] Tout les champs ne sont pas remplis")
      # return error_response("BACK", "routes/auth.py", "login()", "Tout les champs ne sont pas remplis", 400)
    # Vérifier si l'utilisateur existe (par email OU username) → sinon error_response
      # app.logger.error(f"[BACK][routes/auth.py][login()] Le champs username est incorrecte")
      # return error_response("BACK", "routes/auth.py", "login()", "Le champs username est incorrecte", 400)
    # Vérifier le mdp → sinon error_response
      # app.logger.error(f"[BACK][routes/auth.py][login()] Le mot de passe est incorrecte")
      # return error_response("BACK", "routes/auth.py", "login()", "Le mot de passe est incorrecte", 400)
    # Générer un access_token et un refresh_token JWT
    # Retourner les tokens dans la réponse (et en cookie httpOnly si activé)
    # Si tout est Ok → success_response + logger.info
    app.logger.info(f"[BACK][routes/auth.py][login()] Le user à été connecté avec succès")
    return success_response("BACK", "routes/auth.py", "login()", "Le user à été connecté avec succès", {data}, 201)


# --------------------------------------------------- Route POST : /auth/logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Vérifier si le token est valide → sinon error_response
    # Supprimer/invalider les cookies JWT (unset_jwt_cookies)
      # app.logger.error(f"[BACK][routes/auth.py][logout()] Le clean des cookies et token à échoué")
      # return error_response("BACK", "routes/auth.py", "logout()", "Le clean des cookies et token à échoué", 400)
    # Si tout est Ok → success_response + logger.info
    app.logger.info(f"[BACK][routes/auth.py][logout()] Le clean des cookies et token à été un succès")
    return success_response("BACK", "routes/auth.py", "logout()", "Le clean des cookies et token à été un succès", 201)

# ---------------------------------------------- Route POST & PUT : /auth/reset
@auth_bp.route('/reset', methods=['POST'])
def reset_request():
    data = request.get_json()
    # Vérifier si l'email est fourni → sinon error_response
    # app.logger.error(f"[BACK][routes/auth.py][reset_request()] Le champ email est vide")
    # return error_response("BACK", "routes/auth.py", "reset_request()", "Le champ email est vide", 400)
    # Vérifier si user existe dans la DB → sinon error_response
    # app.logger.error(f"[BACK][routes/auth.py][reset_request()] L'email entré n'existe pas")
    # return error_response("BACK", "routes/auth.py", "reset_request()", "L'email entré n'existe pas", 400)
    # Générer un token temporaire
    # Sauvegarder le token en DB (lié à l'user, avec expiration)
    app.logger.info(f"[BACK][routes/auth.py][reset_request()] Lien de réinitialisation généré avec succès")
    return success_response("BACK", "routes/auth.py", "reset_request()", "Lien de réinitialisation généré avec succès (MVP : token renvoyé dans la réponse).", {"reset_token": "TOKEN_EXEMPLE"}, 200)

@auth_bp.route('/reset/<token>', methods=['PUT'])
def reset_confirm(token):
    data = request.get_json()
    # Vérifier si le token est valide → sinon error_response
    # app.logger.error(f"[BACK][routes/auth.py][reset_confirm()] Le token n'est pas valide")
    # return error_response("BACK", "routes/auth.py", "reset_confirm()", "Le token n'est pas valide", 400)
    # Vérifier si le champ "new_password" est fourni et conforme → sinon error_response
    # app.logger.error(f"[BACK][routes/auth.py][reset_confirm()] Le champ new_password est vide")
    # return error_response("BACK", "routes/auth.py", "reset_confirm()", "Le champ new_password est vide", 400)
    # Hasher le nouveau mot de passe
    # Mettre à jour l'user dans la DB
    # Invalider le token en DB
    app.logger.info(f"[BACK][routes/auth.py][reset_confirm()] Mot de passe mis à jour avec succès.")
    return success_response("BACK", "routes/auth.py", "reset_confirm()", "Mot de passe mis à jour avec succès.", 200)

@auth_bp.route('/reset', methods=['PUT'])
@jwt_required()
def update_password():
    # Vérifier si le token est valide → sinon error_response
    # Sinon envoie de error_response et app.logger
    # app.logger.error(f"[BACK][routes/auth.py][update_password()] La modification du mdp à échoué")
    # return error_response("BACK", "routes/auth.py", "update_password()", "La modification du mdp à échoué", 400)
    # Vérifier si l'ancien mdp est fourni' → sinon error_response
    # app.logger.error(f"[BACK][routes/auth.py][update_password()] La modification du mdp à échoué")
    # return error_response("BACK", "routes/auth.py", "update_password()", "La modification du mdp à échoué", 400)
    # Vérifier si l'ancien mdp est le bon → sinon error_response
    # app.logger.error(f"[BACK][routes/auth.py][update_password()] La modification du mdp à échoué")
    # return error_response("BACK", "routes/auth.py", "update_password()", "La modification du mdp à échoué", 400)
    # Si c'est Ok alors le mdp est modifié en bbd
    app.logger.info(f"[BACK][routes/auth.py][update_password()] La modification du mdp à été un succès")
    return success_response("BACK", "routes/auth.py", "update_password()", "La modification du mdp à été un succès", 201)

# --------------------------------------------- Route GET & PUT : /auth/profile
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def show_profile():
    # Vérifier si le token est valide → sinon error_response
    # Sinon envoie de error_response et app.logger
    # app.logger.error(f"[BACK][routes/auth.py][show_profile()] Le user n'est pas connecté pour afficher son profile")
    # return error_response("BACK", "routes/auth.py", "show_profile()", "Le user n'est pas connecté pour afficher son profile", 400)
    app.logger.info(f"[BACK][routes/auth.py][show_profile()] L'affichage du profile du user est un succes")
    return success_response("BACK", "routes/auth.py", "show_profile()", "L'affichage du profile du user est un succes", 201)

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    # Vérifier si le token est valide → sinon error_response
    # Sinon envoie de error_response et app.logger
    # app.logger.error(f"[BACK][routes/auth.py][update_profile()] Le user n'est pas connecté pour modifier son profile")
    # return error_response("BACK", "routes/auth.py", "update_profile()", "Le user n'est pas connecté pour modifier son profile", 400)
    # Vérifier si les champs modifiés fournis sont conforme → sinon error_response
    # Sinon envoie de error_response et app.logger
    # app.logger.error(f"[BACK][routes/auth.py][update_profile()] Les champs sont incorrectes : La modification du profile à échoué")
    # return error_response("BACK", "routes/auth.py", "update_profile()", "Les champs sont incorrectes : La modification du profile à échoué", 400)
    app.logger.info(f"[BACK][routes/auth.py][update_profile()] La modification du profile à été un succès")
    return success_response("BACK", "routes/auth.py", "update_profile()", "La modification du profile à été un succès", 201)
