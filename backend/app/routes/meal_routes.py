"""
[BACK][routes/meal_routes.py]

Blueprint : meal_bp — prefix /data/meal
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /              Create a new meal entry
  GET    /              Retrieve meal entries (time range filter)
  PUT    /<entry_id>    Update a meal entry
  DELETE /<entry_id>    Delete a meal entry

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
from app.services import meal_service

meal_bp = Blueprint('meal', __name__, url_prefix='/data/meal')


@meal_bp.route('/', methods=['POST'])
@jwt_required()
def create_meal_entry_route():
    """Create a new meal entry for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        new_entry = meal_service.create_meal_entry(user_id, data)
        app.logger.info(f"[BACK][routes/meal_service.py][create_meal_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/meal_routes.py][create_meal_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_routes.py][create_meal_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@meal_bp.route('/', methods=['GET'])
@jwt_required()
def get_meal_entry_route():
    """Retrieve meal entries for a given date range."""
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = meal_service.get_meal_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/meal_service.py][get_meal_entry_route()] {len(entries)} repas récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/meal_routes.py][get_meal_entry_route] Paramètre invalide : {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_routes.py][get_meal_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@meal_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_meal_entry_route(entry_id):
    """Update an existing meal entry."""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({"error": "Missing request body"}), 400

        update_data = meal_service.update_meal_entry(user_id, entry_id, new_data)
        if not update_data:
            return jsonify({"error": "Meal entry not found"}), 404

        app.logger.info(f"[BACK][routes/meal_routes.py][update_meal_entry_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/meal_routes.py][update_meal_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_routes.py][update_meal_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@meal_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_entry_route(entry_id):
    """Delete a meal entry."""
    try:
        user_id = get_jwt_identity()
        result = meal_service.delete_meal_entry(entry_id, user_id)
        if not result:
            return jsonify({"error": "Meal entry not found"}), 404

        app.logger.info(f"[BACK][routes/meal_service.py][delete_meal_entry_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 204

    except Exception as e:
        app.logger.error(f"[BACK][routes/meal_routes.py][delete_meal_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
