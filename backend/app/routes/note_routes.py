from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import note_service

note_bp = Blueprint('note', __name__, url_prefix='/data/health_professionals/<health_professional_id>/notes')


@note_bp.route('/', methods=['POST'])
@jwt_required()
def create_note_entry_route(health_professional_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = note_service.create_note_entry(user_id, health_professional_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_note_entry_route] Nouvelle note créée pour user {user_id}, pro {health_professional_id}")
        return jsonify(new_entry.to_dict()), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_note_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@note_bp.route('/', methods=['GET'])
@jwt_required()
def get_note_entries_route(health_professional_id):
    try:
        user_id = get_jwt_identity()
        entries = note_service.get_note_entries(user_id, health_professional_id)
        app.logger.info(f"[BACK][routes/data.py][get_note_entries_route] {len(entries)} notes récupérées pour user {user_id}, pro {health_professional_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_note_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@note_bp.route('/<notes_id>', methods=['PUT'])
@jwt_required()
def update_note_entry_route(health_professional_id, notes_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = note_service.update_note_entry(user_id, health_professional_id, notes_id, new_data)
        if not update_data:
            return jsonify({"message": "Note introuvable."}), 404
        app.logger.info(f"[BACK][routes/data.py][update_note_entry_route] Note {notes_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_note_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@note_bp.route('/<notes_id>', methods=['DELETE'])
@jwt_required()
def delete_note_entry_route(health_professional_id, notes_id):
    try:
        user_id = get_jwt_identity()
        result = note_service.delete_note_entry(user_id, health_professional_id, notes_id)
        if not result:
            return jsonify({"message": "Note introuvable."}), 404
        app.logger.info(f"[BACK][routes/data.py][delete_note_entry_route] Note {notes_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_note_entry_route] Erreur inattendue lors de la suppression : {e}")
        return jsonify({"error": str(e)}), 500
