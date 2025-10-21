from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services import auth_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user account (public route)."""
    try:
        data = request.get_json()
        new_user = auth_service.create_user(data)
        app.logger.info("[BACK][routes/auth_routes.py][register] Le nouvel utilisateur à été enregistré avec succès")
        return jsonify(new_user), 201

    except ValueError as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][register()] Données invalides pour le nouvel utilisateur: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth_routes.py][register()] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user credentials and generate JWT tokens (public route)."""
    try:
        data = request.get_json()
        remember_me = data.get("remember_me", False)
        validated = auth_service.validate_login_data(data)
        app.logger.info(f"[BACK][routes/auth.py][login] Les données de connexion sont valides")
        user = auth_service.find_user_by_email_or_username(validated)
        app.logger.info(f"[BACK][routes/auth.py][login] Utilisateur trouvé par son email ou son username")
        auth_service.authenticate_user(user, validated["password"])
        app.logger.info(f"[BACK][routes/auth.py][login] Le mot de passe pour l'utilisateur: {user.id} est valide")

        if user.first_login:
            user.first_login = False
            user.save()
            app.logger.info(f"[BACK][routes/auth.py][login] Première connexion détectée pour l'utilisateur: {user.email}")
        else:
            app.logger.info(f"[BACK][routes/auth.py][login] L'utilisateur: {user.id} est connecté")
        return auth_service.generate_tokens(user, remember_me)

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


@auth_bp.route('/reset', methods=['POST'])
def reset_request():
    """Request a password reset link by providing a valid email (public route)."""
    try:
        data = request.get_json()
        email = auth_service.validate_reset_request(data)
        user = auth_service.find_user_by_email(email)
        response = auth_service.generate_reset_token(user)
        auth_service.send_reset_email(user, response.get_json().get("message"))
        app.logger.info(f"[BACK][routes/auth.py][reset_request] L'email de réinitialisation du mot de passe de l'utilisateur: {user.email} a bien été envoyé")
        return response

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
        data = request.get_json()
        decoded_token = auth_service.validate_reset_token(token)
        user = auth_service.find_user_by_email(decoded_token["sub"])
        auth_service.update_user_password(user, data["new_password"])
        auth_service.clear_reset_token()
        app.logger.info(f"[BACK][routes/auth.py][reset_confirm()] Password updated successfully for {user.email}")
        return jsonify({"message": "Password updated successfully"}), 200
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
        data = request.get_json()
        current_user = auth_service.get_user_from_identity()
        auth_service.update_user_password(current_user, data["new_password"])
        app.logger.info(f"[BACK][routes/auth.py][update_password()] Password updated successfully for {current_user.email}")
        return jsonify({"message": "Password updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][update_password()] Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def show_profile():
    """Retrieve the current user's profile information (JWT required)."""
    current_user = auth_service.get_user_from_identity()
    cleaned_user = auth_service.sanitize_user_profile(current_user)
    app.logger.info(f"[BACK][routes/auth.py][show_profile()] Profile retrieved successfully for {current_user.email}")
    return jsonify(cleaned_user), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the current user's profile information in the database (JWT required)."""
    try:
        data = request.get_json()
        current_user = auth_service.get_user_from_identity()
        updated_user = auth_service.update_profile(current_user, data)
        app.logger.info(f"[BACK][routes/auth.py][update_profile()] Profile updated successfully for {current_user.email}")
        return jsonify(updated_user), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/auth.py][update_profile()] Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


