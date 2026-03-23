"""
[BACK][routes/note_routes.py]

Blueprint : note_bp — prefix /data/health_professionals/<health_professional_id>/notes
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /              Create a new note for a health professional
  GET    /              Retrieve all notes for a health professional
  PUT    /<notes_id>    Update a note
  DELETE /<notes_id>    Delete a note

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
from app.services import note_service

note_bp = Blueprint('note', __name__, url_prefix='/data/health_professionals/<health_professional_id>/notes')


@note_bp.route('/', methods=['POST'])
@jwt_required()
def create_note_entry_route(health_professional_id):
    """Create a new note for a health professional."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        new_entry = note_service.create_note_entry(user_id, health_professional_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_note_entry_route] Nouvelle note créée pour user {user_id}, pro {health_professional_id}")
        return jsonify(new_entry.to_dict()), 201

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/note_routes.py][create_note_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/note_routes.py][create_note_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@note_bp.route('/', methods=['GET'])
@jwt_required()
def get_note_entries_route(health_professional_id):
    """Retrieve all notes for a given health professional."""
    try:
        user_id = get_jwt_identity()
        entries = note_service.get_note_entries(user_id, health_professional_id)
        app.logger.info(f"[BACK][routes/data.py][get_note_entries_route] {len(entries)} notes récupérées pour user {user_id}, pro {health_professional_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/note_routes.py][get_note_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@note_bp.route('/<notes_id>', methods=['PUT'])
@jwt_required()
def update_note_entry_route(health_professional_id, notes_id):
    """Update a note."""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({"error": "Missing request body"}), 400

        update_data = note_service.update_note_entry(user_id, health_professional_id, notes_id, new_data)
        if not update_data:
            return jsonify({"error": "Note not found"}), 404

        app.logger.info(f"[BACK][routes/note_routes.py][update_note_entry_route] Note {notes_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/note_routes.py][update_note_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/note_routes.py][update_note_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@note_bp.route('/<notes_id>', methods=['DELETE'])
@jwt_required()
def delete_note_entry_route(health_professional_id, notes_id):
    """Delete a note."""
    try:
        user_id = get_jwt_identity()
        result = note_service.delete_note_entry(user_id, health_professional_id, notes_id)
        if not result:
            return jsonify({"message": "Note introuvable."}), 404

        app.logger.info(f"[BACK][routes/data.py][delete_note_entry_route] Note {notes_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 204

    except Exception as e:
        app.logger.error(f"[BACK][routes/note_routes.py][delete_note_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
