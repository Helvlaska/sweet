from  flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import data_service

data_bp = Blueprint('data', __name__, url_prefix='/data')

# ------------------------------------------------------- Routes glycemia
@data_bp.route('/glycemia', methods=['POST'])
@jwt_required()
def create_glycemia_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_glycemia_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_glycemia_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_glycemia_entry_route()] Erreur inattendue pour l'entré d'une nouvelle mesure : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/glycemia', methods=['GET'])
@jwt_required()
def get_glycemia_entries_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_glycemia_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_entries_route()] {len(entries)} mesures récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_glycemia_entries_route()] Erreur inattendue pour la récupération des mesures : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/glycemia/stats', methods=['GET'])
@jwt_required()
def get_glycemia_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = data_service.get_glycemia_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_stats_route()] Moyenne glycémique récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_glycemia_stats_route()] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/glycemia/<entry_id>', methods=['PUT'])
@jwt_required()
def update_glycemia_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_glycemia_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_glycemia_entry_route()] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_glycemia_entry_route()] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/glycemia/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_glycemia_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_glycemia_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_glycemia_entry_route()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_glycemia_entry_route()] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------- Routes weight
@data_bp.route('/weight', methods=['POST'])
@jwt_required()
def create_weight_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_weight_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_weight_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_weight_entry_route()] Erreur inattendue pour l'entré d'une nouvelle mesure : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/weight', methods=['GET'])
@jwt_required()
def get_weight_entries_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_weight_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_weight_entries_route()] {len(entries)} mesures récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_weight_entries_route()] Erreur inattendue pour la récupération des mesures : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/weight/stats', methods=['GET'])
@jwt_required()
def get_weight_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = data_service.get_weight_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_weight_stats_route()] Moyenne de poids récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_weight_stats_route()] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/weight/<entry_id>', methods=['PUT'])
@jwt_required()
def update_weight_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_weight_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_weight_entry_route()] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_weight_entry_route()] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/weight/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_weight_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_weight_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_weight_entry_route()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_weight_entry_route()] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------- Routes activity
@data_bp.route('/activity', methods=['POST'])
@jwt_required()
def create_activity_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_activity_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_activity_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_activity_entry_route] Erreur inattendue pour l'entré d'une nouvelle activité : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_activity_entry_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_activity_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_activity_entry_route()] {len(entries)} activités récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_activity_entry_route()] Erreur inattendue pour la récupération des activités : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/activity/stats', methods=['GET'])
@jwt_required()
def get_activity_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = data_service.get_activity_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_activity_stats_route] Moyenne de temps d'activité récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_activity_stats_route] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/activity/<entry_id>', methods=['PUT'])
@jwt_required()
def update_activity_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_activity_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_activity_entry_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_activity_entry_route] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/activity/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_activity_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_activity_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_activity_entry_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_activity_entry_route] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------- Routes meal
@data_bp.route('/meal', methods=['POST'])
@jwt_required()
def create_meal_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_meal_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_meal_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_meal_entry_route] Erreur inattendue pour l'entré d'un nouveau repas : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/meal', methods=['GET'])
@jwt_required()
def get_meal_entry_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_meal_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_meal_entry_route()] {len(entries)} repas récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_meal_entry_route()] Erreur inattendue pour la récupération des repas : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/meal/<entry_id>', methods=['PUT'])
@jwt_required()
def update_meal_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_meal_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_meal_entry_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_meal_entry_route] Erreur inattendue pour la modification du repas : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/meal/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_meal_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_meal_entry_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_meal_entry_route] Erreur inattendue lors de la suppression du repas : {e}")
        return jsonify({"error": str(e)}), 500
