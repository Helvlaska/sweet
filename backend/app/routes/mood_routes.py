"""
[BACK][routes/mood_routes.py]

Blueprint : mood_bp — prefix /data/mood
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /              Create a new mood entry
  GET    /              Retrieve mood entries (time range filter)
  PUT    /<entry_id>    Update a mood entry
  DELETE /<entry_id>    Delete a mood entry

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


from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import mood_service

mood_bp = Blueprint('mood', __name__, url_prefix='/data/mood')


@mood_bp.route('/', methods=['POST'])
@jwt_required()
def create_mood_entry_route():
    """Create a new mood entry for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        new_entry = mood_service.create_mood_entry(user_id, data)
        app.logger.info(f"[BACK][routes/mood_routes.py][create_mood_entry_route] Nouvelle humeur '{new_entry.get('description')}' créée pour user {user_id}")
        return jsonify(new_entry), 201

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][create_mood_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][create_mood_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@mood_bp.route('/', methods=['GET'])
@jwt_required()
def get_mood_entry_route():
    """Retrieve mood entries for a given date range."""
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = mood_service.get_mood_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/mood_routes.py][get_mood_entry_route] {len(entries)} humeurs récupérées pour user {user_id}, période {range_type}")
        return jsonify(entries), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/mood_routes.py][get_mood_entry_route] Paramètre invalide : {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][get_mood_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@mood_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_mood_entry_route(entry_id):
    """Update an existing mood entry."""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({"error": "Missing request body"}), 400

        update_data = mood_service.update_mood_entry(user_id, entry_id, new_data)
        if not update_data:
            return jsonify({"error": "Mood entry not found"}), 404

        app.logger.info(f"[BACK][routes/mood_routes.py][update_mood_entry_route] Humeur {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][update_mood_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][update_mood_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@mood_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_mood_entry_route(entry_id):
    """Delete a mood entry."""
    try:
        user_id = get_jwt_identity()
        result = mood_service.delete_mood_entry(entry_id, user_id)
        if not result:
            return jsonify({"error": "Mood entry not found"}), 404

        app.logger.info(f"[BACK][routes/mood_routes.py][delete_mood_entry_route] Humeur {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 204

    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][delete_mood_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
