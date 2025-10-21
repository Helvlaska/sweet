from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import mood_service

mood_bp = Blueprint('mood', __name__, url_prefix='/data/mood')


@mood_bp.route('/', methods=['POST'])
@jwt_required()
def create_mood_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = mood_service.create_mood_entry(user_id, data)
        app.logger.info(f"[BACK][routes/mood_routes.py][create_mood_entry_route] Nouvelle humeur '{new_entry.get('description')}' créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][create_mood_entry_route] Erreur inattendue lors de la création d'une nouvelle humeur : {e}")
        return jsonify({"error": str(e)}), 500


@mood_bp.route('/', methods=['GET'])
@jwt_required()
def get_mood_entry_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = mood_service.get_mood_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/mood_routes.py][get_mood_entry_route] {len(entries)} humeurs récupérées pour user {user_id}, période {range_type}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][get_mood_entry_route] Erreur inattendue lors de la récupération des humeurs : {e}")
        return jsonify({"error": str(e)}), 500


@mood_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_mood_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = mood_service.update_mood_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/mood_routes.py][update_mood_entry_route] Humeur {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][update_mood_entry_route] Erreur inattendue lors de la mise à jour de l’humeur : {e}")
        return jsonify({"error": str(e)}), 500


@mood_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_mood_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = mood_service.delete_mood_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/mood_routes.py][delete_mood_entry_route] Humeur {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/mood_routes.py][delete_mood_entry_route] Erreur inattendue lors de la suppression de l’humeur : {e}")
        return jsonify({"error": str(e)}), 500
