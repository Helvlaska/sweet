"""
[BACK][routes/medication_routes.py]

Blueprint : medication_bp — prefix /data/medication
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /                    Create a new medication entry
  GET    /                    Retrieve all medications for the user
  PUT    /<entry_id>          Update a medication entry
  DELETE /<entry_id>          Delete a medication entry
  PATCH  /<entry_id>/take     Record a medication dose intake

HTTP status codes:
  201  Resource created
  200  Success (read / update / take dose)
  204  Success (delete, no content)
  400  Missing or malformed data
  401  Missing or invalid token
  404  Resource not found
  422  Data present but invalid (wrong type, out of range, insufficient stock)
  500  Unexpected server error
"""


from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import medication_service

medication_bp = Blueprint('medication', __name__, url_prefix='/data/medication')


@medication_bp.route('/', methods=['POST'])
@jwt_required()
def create_medication_entry_route():
    """Create a new medication entry for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        new_entry = medication_service.create_medication_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_medication_entry_route] Nouveau médicament '{new_entry.get('name')}' ajouté pour user {user_id}")
        return jsonify(new_entry), 201

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][create_medication_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][create_medication_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@medication_bp.route('/', methods=['GET'])
@jwt_required()
def get_medication_entry_route():
    """Retrieve all medications for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        entries = medication_service.get_medication_entry(user_id)
        app.logger.info(f"[BACK][routes/data.py][get_medication_entry_route] {len(entries)} médicaments récupérés pour user {user_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][get_medication_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@medication_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_medication_entry_route(entry_id):
    """Update an existing medication entry."""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({"error": "Missing request body"}), 400

        updated_entry = medication_service.update_medication_entry(user_id, entry_id, new_data)
        if not updated_entry:
            return jsonify({"error": "Medication not found"}), 404

        app.logger.info(f"[BACK][routes/medication_routes.py][update_medication_entry_route] Médicament {entry_id} mis à jour pour user {user_id}")
        return jsonify(updated_entry), 200

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][update_medication_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][update_medication_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@medication_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_medication_entry_route(entry_id):
    """Delete a medication entry."""
    try:
        user_id = get_jwt_identity()
        result = medication_service.delete_medication_entry(entry_id, user_id)
        if not result:
            return jsonify({"error": "Medication not found"}), 404

        app.logger.info(f"[BACK][routes/data.py][delete_medication_entry_route] Médicament {entry_id} supprimé pour user {user_id}")
        return jsonify(result), 204

    except Exception as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][delete_medication_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@medication_bp.route('/<entry_id>/take', methods=['PATCH'])
@jwt_required()
def take_medication_dose_route(entry_id):
    """Record a medication dose intake — decrements stock."""
    try:
        user_id = get_jwt_identity()
        updated_entry = medication_service.take_medication_dose(user_id, entry_id)
        if not updated_entry:
            app.logger.error("[BACK][routes/data.py][take_medication_dose_route] Médicament introuvable")
            return jsonify({"error": "Médicament introuvable"}), 404

        app.logger.info(f"[BACK][routes/data.py][take_medication_dose_route] Prise enregistrée pour user {user_id} sur médicament {entry_id}")
        return jsonify(updated_entry), 200

    except ValueError as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][take_medication_dose_route] Stock insuffisant : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/medication_routes.py][take_medication_dose_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
