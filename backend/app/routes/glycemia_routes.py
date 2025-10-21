from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import glycemia_service

glycemia_bp = Blueprint('glycemia', __name__, url_prefix='/data/glycemia')


@glycemia_bp.route('/', methods=['POST'])
@jwt_required()
def create_glycemia_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = glycemia_service.create_glycemia_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_glycemia_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_glycemia_entry_route()] Erreur inattendue pour l'entré d'une nouvelle mesure : {e}")
        return jsonify({"error": str(e)}), 500


@glycemia_bp.route('/', methods=['GET'])
@jwt_required()
def get_glycemia_entries_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = glycemia_service.get_glycemia_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_entries_route()] {len(entries)} mesures récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_glycemia_entries_route()] Erreur inattendue pour la récupération des mesures : {e}")
        return jsonify({"error": str(e)}), 500


@glycemia_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_glycemia_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = glycemia_service.get_glycemia_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_stats_route()] Moyenne glycémique récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_glycemia_stats_route()] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500


@glycemia_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_glycemia_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = glycemia_service.update_glycemia_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_glycemia_entry_route()] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_glycemia_entry_route()] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


@glycemia_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_glycemia_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = glycemia_service.delete_glycemia_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_glycemia_entry_route()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_glycemia_entry_route()] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500
