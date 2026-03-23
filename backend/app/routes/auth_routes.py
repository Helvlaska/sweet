"""
[BACK][routes/auth_routes.py]

Blueprint : auth_bp — prefix /auth
Authentication : JWT required on protected routes (@jwt_required)

Exposed routes:
  POST   /register                 Register a new user account
  POST   /check-availability       Check email / username availability
  POST   /login                    Authenticate and generate JWT tokens
  POST   /logout                   Clear JWT cookies
  POST   /refresh                  Refresh access token
  POST   /onboarding/complete      Mark onboarding as complete
  POST   /reset                    Request a password reset link
  PUT    /reset/<token>            Confirm password reset with token
  PUT    /password                 Update password while authenticated
  GET    /profile                  Retrieve current user profile
  PUT    /profile                  Update current user profile

HTTP status codes:
  201  Resource created
  200  Success (read / update)
  400  Missing or malformed data
  401  Missing, invalid or expired token / wrong credentials
  404  Resource not found
  422  Data present but invalid (out of range, wrong type)
  500  Unexpected server error
"""


from flask import current_app as app, Blueprint, make_response, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError
from app.services import auth_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user account (public route)."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        new_user = auth_service.create_user(data)
        app.logger.info("[BACK][routes/auth_routes.py][register] Le nouvel utilisateur à été enregistré avec succès")
        return jsonify(new_user), 201

    except IntegrityError as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][register] Contrainte base de données : {e}")
        return jsonify({"error": "Missing or duplicate field"}), 422
    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][register()] Données invalides pour le nouvel utilisateur: {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][register()] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/check-availability', methods=['POST'])
def check_availability_route():
    """Check email and username availability (public route)."""
    try:
        data = request.get_json()
        if not data:
                return jsonify({"error": "Missing request body"}), 400

        result = auth_service.check_availability(data)
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][check_availability_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/onboarding/complete', methods=['POST'])
@jwt_required()
def complete_onboarding():
    """Mark onboarding as complete for the current user (JWT required)."""
    try:
        user_id = get_jwt_identity()
        auth_service.complete_first_login(user_id)
        return jsonify({"message": "Onboarding terminé"}), 200

    except ValueError as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][complete_onboarding] Utilisateur introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][complete_onboarding] Erreur : {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user credentials and generate JWT tokens (public route)."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        remember_me = data.get("remember_me", False)
        validated = auth_service.validate_login_data(data)
        app.logger.info(f"[BACK][routes/auth.py][login] Les données de connexion sont valides")
        user = auth_service.find_user_by_email_or_username(validated)
        app.logger.info(f"[BACK][routes/auth.py][login] Utilisateur trouvé par son email ou son username")
        auth_service.authenticate_user(user, validated["password"])
        app.logger.info(f"[BACK][routes/auth.py][login] Le mot de passe pour l'utilisateur: {user.id} est valide")

        app.logger.info(f"[BACK][routes/auth.py][login] L'utilisateur: {user.id} est connecté")
        return auth_service.generate_tokens(user, remember_me)

    except KeyError as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][login] Champ manquant : {e}")
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except ValueError as e:
        app.logger.error(f"[BACK][routes/auth.py][login] Invalid credentials: {e}")
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][login] Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout the current user and clear all JWT cookies (JWT required)."""
    app.logger.info(f"[BACK][routes/auth.py][logout] Demande de déconnexion reçue")
    return auth_service.logout_user()


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Regenerate an access token from the refresh token (JWT refresh required)."""
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        response = make_response(jsonify({"message": "Access token refreshed"}), 200)
        set_access_cookies(response, new_access_token)
        app.logger.info(f"[BACK][routes/auth_routes.py][refresh()] Nouveau access_token généré pour user_id={current_user_id}")
        return response

    except Exception as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][refresh()] Erreur lors du refresh : {str(e)}")
        return jsonify({"error": "Impossible de régénérer le token"}), 401


@auth_bp.route('/reset', methods=['POST'])
def reset_request():
    """Request a password reset link by providing a valid email (public route)."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        email = auth_service.validate_reset_request(data)
        user = auth_service.find_user_by_email(email)
        if not user:
            app.logger.info(f"[BACK][routes/auth_routes.py][reset_request] Email non trouvé: réponse neutre envoyée (anti-énumération)")
            return jsonify({"message": "Si un compte est associé à cette adresse, vous recevrez un email"}), 200

        reset_token = auth_service.generate_reset_token(user)
        auth_service.send_reset_email(user, reset_token)
        app.logger.info(f"[BACK][routes/auth.py][reset_request] L'email de réinitialisation du mot de passe de l'utilisateur: {user.email} a bien été envoyé")
        return jsonify({"message": "Si un compte est associé à cette adresse, vous recevrez un email"}), 200

    except ValueError as e:
        app.logger.error(f"[BACK][routes/auth.py][reset_request] Données pour la requête de rénitialisation invalides: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][reset_request] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/reset/<token>', methods=['PUT'])
def reset_confirm(token):
    """Confirm password reset using a temporary token received by email (public route)."""
    try:
        data = request.get_json(silent=True)
        if not data or "new_password" not in data:
            return jsonify({"error": "Missing field: new_password"}), 400

        decoded_token = auth_service.validate_reset_token(token)
        user = auth_service.find_user_by_email(decoded_token["sub"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        auth_service.update_user_password(user, data["new_password"])
        auth_service.clear_reset_token()
        app.logger.info(f"[BACK][routes/auth.py][reset_confirm()] Password updated successfully for {user.email}")
        return jsonify({"message": "Password updated successfully"}), 200

    except ExpiredSignatureError:
        app.logger.error("[BACK][routes/auth_routes.py][reset_confirm] Token expiré")
        return jsonify({"error": "Reset token has expired"}), 401
    except InvalidTokenError:
        app.logger.error("[BACK][routes/auth_routes.py][reset_confirm] Token invalide")
        return jsonify({"error": "Invalid reset token"}), 401
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][reset_confirm()] Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/password', methods=['PUT'])
@jwt_required()
def update_password():
    """Update the current user's password while authenticated (JWT required)."""
    try:
        data = request.get_json(silent=True)
        if not data or "new_password" not in data:
            return jsonify({"error": "Missing field: new_password"}), 400

        current_user = auth_service.get_user_from_identity()
        if not current_user:
            return jsonify({"error": "User not found"}), 404

        auth_service.update_user_password(current_user, data["new_password"])
        app.logger.info(f"[BACK][routes/auth.py][update_password()] Password updated successfully for {current_user.email}")
        return jsonify({"message": "Password updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][update_password()] Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def show_profile():
    """Retrieve the current user's profile information (JWT required)."""
    try:
        current_user = auth_service.get_user_from_identity()
        if not current_user:
            return jsonify({"error": "User not found"}), 404

        cleaned_user = auth_service.sanitize_user_profile(current_user)
        app.logger.info(f"[BACK][routes/auth.py][show_profile()] Profile retrieved successfully for {current_user.email}")
        return jsonify(cleaned_user), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][show_profile] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the current user's profile information in the database (JWT required)."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        current_user = auth_service.get_user_from_identity()
        if not current_user:
            return jsonify({"error": "User not found"}), 404

        updated_user = auth_service.update_profile(current_user, data)
        app.logger.info(f"[BACK][routes/auth.py][update_profile()] Profile updated successfully for {current_user.email}")
        return jsonify(updated_user), 200

    except ValueError as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][update_profile] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][update_profile()] Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


