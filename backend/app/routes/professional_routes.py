from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import professional_service

professional_bp = Blueprint('health_professional', __name__, url_prefix='/data/health_professionals')


@professional_bp.route('/', methods=['POST'])
@jwt_required()
def create_health_professional_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = professional_service.create_health_professional_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_health_professional_entry_route] Nouveau professionnel créé pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@professional_bp.route('/', methods=['GET'])
@jwt_required()
def get_health_professional_entries_route():
    try:
        user_id = get_jwt_identity()
        entries = professional_service.get_health_professional_entries(user_id)
        app.logger.info(f"[BACK][routes/data.py][get_health_professional_entries_route] {len(entries)} professionnels récupérés pour user {user_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_health_professional_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500

@professional_bp.route('/<health_professionals_id>/notes', methods=['GET'])
@jwt_required()
def get_health_professional_with_notes_route(health_professionals_id):
    try:
        user_id = get_jwt_identity()
        result = professional_service.get_health_professional_with_notes(user_id, health_professionals_id)
        if not result:
            return jsonify({"message": "Aucun professionnel trouvé pour cet utilisateur."}), 404
        app.logger.info(f"[BACK][routes/data.py][get_health_professional_with_notes_route] Données pro+notes envoyées pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_health_professional_with_notes_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500



@professional_bp.route('/<health_professionals_id>', methods=['PUT'])
@jwt_required()
def update_health_professional_entry_route(health_professionals_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = professional_service.update_health_professional_entry(user_id, health_professionals_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_health_professional_entry_route] Entrée {health_professionals_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@professional_bp.route('/<health_professionals_id>', methods=['DELETE'])
@jwt_required()
def delete_health_professional_entry_route(health_professionals_id):
    try:
        user_id = get_jwt_identity()
        result = professional_service.delete_health_professional_entry(health_professionals_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_health_professional_entry_route] Entrée {health_professionals_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500
