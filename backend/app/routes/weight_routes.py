from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import weight_service

weight_bp = Blueprint('weight', __name__, url_prefix='/data/weight')


@weight_bp.route('/', methods=['POST'])
@jwt_required()
def create_weight_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = weight_service.create_weight_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_weight_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_weight_entry_route()] Erreur inattendue pour l'entré d'une nouvelle mesure : {e}")
        return jsonify({"error": str(e)}), 500


@weight_bp.route('/', methods=['GET'])
@jwt_required()
def get_weight_entries_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = weight_service.get_weight_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_weight_entries_route()] {len(entries)} mesures récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_weight_entries_route()] Erreur inattendue pour la récupération des mesures : {e}")
        return jsonify({"error": str(e)}), 500


@weight_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_weight_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = weight_service.get_weight_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_weight_stats_route()] Moyenne de poids récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_weight_stats_route()] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500


@weight_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_weight_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = weight_service.update_weight_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_weight_entry_route()] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_weight_entry_route()] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


@weight_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_weight_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = weight_service.delete_weight_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_weight_entry_route()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_weight_entry_route()] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500
