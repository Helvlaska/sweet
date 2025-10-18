from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import activity_service

activity_bp = Blueprint('activity', __name__, url_prefix='/data/activity')

@activity_bp.route('/', methods=['POST'])
@jwt_required()
def create_activity_route():
    """Create a new activity entry for the authenticated user"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error(f"[BACK][routes/activity_routes][create_activity_route] Aucune donnée reçue")
            return jsonify({"error": "Missing JSON data"}), 400
        new_entry = activity_service.create_activity_entry(user_id, data)
        app.logger.info(f"[BACK][routes/activity_routes][create_activity_route] Nouvelle activité {new_entry} créée pour user {user_id}")
        return jsonify(new_entry), 201

    except ValueError as e:
        app.logger.warning(f"[BACK][activity_routes][create_activity_route] Données de l'activité NOK: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][activity_routes][create_activity_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@activity_bp.route('/', methods=['GET'])
@jwt_required()
def get_activity_route():
    """Retrieve activity entries for a given date range"""
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = activity_service.get_activity_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/activity_routes][get_activity_route] {len(entries)} activités récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][activity_routes][get_activity_route] Erreur Date ou Timelaps: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][activity_routes][get_activity_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@activity_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_activity_stats_route():
    """Return average activity duration over a period"""
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = activity_service.get_activity_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/activity_routes][get_activity_stats_route] Moyenne de temps d'activité récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/activity_routes][get_activity_stats_route] Erreur sur les valeurs entrées: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/activity_routes][get_activity_stats_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@activity_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_activity_route(entry_id):
    """Update an existing activity entry"""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "Missing JSON data"}), 400
        update_data = activity_service.update_activity_entry(user_id, entry_id, new_data)
        if not update_data:
            return jsonify({"error": "Activity not found"}), 404
        app.logger.info(f"[BACK][routes/activity_routes][update_activity_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/activity_routes][update_activity_route] Erreur sur les valeurs entrées: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/activity_routes][update_activity_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@activity_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_activity_route(entry_id):
    """Delete a specific activity entry"""
    try:
        user_id = get_jwt_identity()
        result = activity_service.delete_activity_entry(entry_id, user_id)
        if not result:
            app.logger.error("[BACK][routes/activity_routes][delete_activity_route] Activité non trouvée")
            return jsonify({"error": "Activity not found"}), 404
        app.logger.info(f"[BACK][routes/activity_routes][delete_activity_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return "", 204

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/activity_routes][delete_activity_route] Erreur sur les valeurs entrées: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/activity_routes][delete_activity_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500
