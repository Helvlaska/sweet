"""
[BACK][routes/glycemia_routes.py]

Blueprint : glycemia_bp — prefix /data/glycemia
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /              Create a new glycemia entry
  GET    /              Retrieve glycemia entries (time range filter)
  GET    /stats         Compute glycemia statistics
  PUT    /<entry_id>    Update a glycemia entry
  DELETE /<entry_id>    Delete a glycemia entry

HTTP status codes:
  201  Resource created
  200  Success (read / update)
  204  Success (delete, no content)
  400  Missing or malformed data
  401  Missing or invalid token
  404  Resource not found
  422  Data present but invalid (out of range, wrong type)
  500  Unexpected server error
"""


from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import glycemia_service

glycemia_bp = Blueprint('glycemia', __name__, url_prefix='/data/glycemia')


@glycemia_bp.route('/', methods=['POST'])
@jwt_required()
def create_glycemia_entry_route():
    """Create a new glycemia entry for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        new_entry = glycemia_service.create_glycemia_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_glycemia_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/glycemia_routes.py][create_glycemia_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/glycemia_routes.py][create_glycemia_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@glycemia_bp.route('/', methods=['GET'])
@jwt_required()
def get_glycemia_entries_route():
    """Retrieve glycemia entries for a given date range."""
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = glycemia_service.get_glycemia_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_entries_route()] {len(entries)} mesures récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/glycemia_routes.py][get_glycemia_entries_route] Paramètre invalide : {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/glycemia_routes.py][get_glycemia_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@glycemia_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_glycemia_stats_route():
    """Compute glycemia statistics for a given date range."""
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = glycemia_service.get_glycemia_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_stats_route()] Moyenne glycémique récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/glycemia_routes.py][get_glycemia_stats_route] Paramètre invalide : {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/glycemia_routes.py][get_glycemia_stats_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@glycemia_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_glycemia_entry_route(entry_id):
    """Update an existing glycemia entry."""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({"error": "Missing request body"}), 400

        update_data = glycemia_service.update_glycemia_entry(user_id, entry_id, new_data)
        if not update_data:
            return jsonify({"error": "Glycemia entry not found"}), 404

        app.logger.info(f"[BACK][routes/data.py][update_glycemia_entry_route()] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/glycemia_routes.py][update_glycemia_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/glycemia_routes.py][update_glycemia_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@glycemia_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_glycemia_entry_route(entry_id):
    """Delete a glycemia entry."""
    try:
        user_id = get_jwt_identity()
        result = glycemia_service.delete_glycemia_entry(entry_id, user_id)
        if not result:
            return jsonify({"error": "Glycemia entry not found"}), 404

        app.logger.info(f"[BACK][routes/data.py][delete_glycemia_entry_route()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 204

    except Exception as e:
        app.logger.error(f"[BACK][routes/glycemia_routes.py][delete_glycemia_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
