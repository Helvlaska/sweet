"""
[BACK][routes/professional_routes.py]

Blueprint : professional_bp — prefix /data/health_professionals
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /                          Create a new health professional entry
  GET    /                          Retrieve all health professionals for the user
  GET    /<health_professionals_id> Retrieve a health professional with notes and documents
  PUT    /<health_professionals_id> Update a health professional entry
  DELETE /<health_professionals_id> Delete a health professional entry

HTTP status codes:
  201  Resource created
  200  Success (read / update)
  204  Success (delete, no content)
  400  Missing or malformed data
  401  Missing or invalid token
  404  Resource not found
  422  Data present but invalid (wrong type or format)
  500  Unexpected server error
"""


from sqlalchemy.exc import IntegrityError
from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import professional_service

professional_bp = Blueprint('health_professional', __name__, url_prefix='/data/health_professionals')


@professional_bp.route('/', methods=['POST'])
@jwt_required()
def create_health_professional_entry_route():
    """Create a new health professional entry for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        new_entry = professional_service.create_health_professional_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_health_professional_entry_route] Nouveau professionnel créé pour user {user_id}")
        return jsonify(new_entry), 201

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][create_health_professional_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except IntegrityError as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][create_health_professional_entry_route] Contrainte base de données : {e}")
        return jsonify({"error": "Missing or duplicate field"}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][create_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@professional_bp.route('/', methods=['GET'])
@jwt_required()
def get_health_professional_entries_route():
    """Retrieve all health professionals for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        entries = professional_service.get_health_professional_entries(user_id)
        app.logger.info(f"[BACK][routes/data.py][get_health_professional_entries_route] {len(entries)} professionnels récupérés pour user {user_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][get_health_professional_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@professional_bp.route('/<health_professionals_id>', methods=['GET'])
@jwt_required()
def get_health_professional_with_details_route(health_professionals_id):
    """Retrieve a health professional with their notes and documents."""
    try:
        user_id = get_jwt_identity()
        result = professional_service.get_health_professional_with_details(user_id, health_professionals_id)
        if not result:
            return jsonify({"message": "Aucun professionnel trouvé pour cet utilisateur."}), 404

        app.logger.info(
            f"[BACK][routes/health_professional.py][get_health_professional_with_details_route] Données complètes envoyées pour user {user_id}"
        )
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][get_health_professional_with_details_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@professional_bp.route('/<health_professionals_id>', methods=['PUT'])
@jwt_required()
def update_health_professional_entry_route(health_professionals_id):
    """Update a health professional entry."""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({"error": "Missing request body"}), 400

        update_data = professional_service.update_health_professional_entry(user_id, health_professionals_id, new_data)
        if not update_data:
            return jsonify({"error": "Health professional not found"}), 404

        app.logger.info(f"[BACK][routes/data.py][update_health_professional_entry_route] Entrée {health_professionals_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][update_health_professional_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][update_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@professional_bp.route('/<health_professionals_id>', methods=['DELETE'])
@jwt_required()
def delete_health_professional_entry_route(health_professionals_id):
    """Delete a health professional entry."""
    try:
        user_id = get_jwt_identity()
        result = professional_service.delete_health_professional_entry(health_professionals_id, user_id)
        if not result:
            return jsonify({"error": "Health professional not found"}), 404

        app.logger.info(f"[BACK][routes/data.py][delete_health_professional_entry_route] Entrée {health_professionals_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 204

    except Exception as e:
        app.logger.error(f"[BACK][routes/professional_routes.py][delete_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
