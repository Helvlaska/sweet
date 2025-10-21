from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import meal_service

meal_bp = Blueprint('meal', __name__, url_prefix='/data/meal')


@meal_bp.route('/', methods=['POST'])
@jwt_required()
def create_meal_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = meal_service.create_meal_entry(user_id, data)
        app.logger.info(f"[BACK][routes/meal_service.py][create_meal_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_service.py][create_meal_entry_route] Erreur inattendue pour l'entré d'un nouveau repas : {e}")
        return jsonify({"error": str(e)}), 500


@meal_bp.route('/', methods=['GET'])
@jwt_required()
def get_meal_entry_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = meal_service.get_meal_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/meal_service.py][get_meal_entry_route()] {len(entries)} repas récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_service.py][get_meal_entry_route()] Erreur inattendue pour la récupération des repas : {e}")
        return jsonify({"error": str(e)}), 500


@meal_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_meal_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = meal_service.update_meal_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/meal_service.py][update_meal_entry_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_service.py][update_meal_entry_route] Erreur inattendue pour la modification du repas : {e}")
        return jsonify({"error": str(e)}), 500


@meal_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = meal_service.delete_meal_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/meal_service.py][delete_meal_entry_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_service.py][delete_meal_entry_route] Erreur inattendue lors de la suppression du repas : {e}")
        return jsonify({"error": str(e)}), 500
