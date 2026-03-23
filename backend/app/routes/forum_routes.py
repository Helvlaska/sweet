"""
[BACK][routes/forum_routes.py]

Blueprint : forum_bp — prefix /forum/posts
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /              Create a new forum post
  GET    /              Retrieve all forum posts
  GET    /<post_id>     Retrieve a forum post with its comments
  PUT    /<post_id>     Update a forum post (author only)
  DELETE /<post_id>     Delete a forum post (author only)
  POST   /<post_id>/like  Toggle like on a forum post

HTTP status codes:
  201  Resource created
  200  Success (read / update / like)
  204  Success (delete, no content)
  400  Missing or malformed data
  401  Missing or invalid token
  403  Authenticated but forbidden (not author or own post)
  404  Resource not found
  422  Data present but invalid (wrong type or format)
  500  Unexpected server error
"""


from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import forum_service

forum_bp = Blueprint('forum', __name__, url_prefix='/forum/posts')


@forum_bp.route("/", methods=["POST"])
@jwt_required()
def route_create_forum_post():
    """Create a new forum post."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            app.logger.error("[BACK][routes/data.py][route_create_forum_post] Requête vide ou invalide")
            return jsonify({"error": "Missing request body"}), 400

        post = forum_service.create_forum_post_entry(current_user_id, data)
        app.logger.info(f"[BACK][routes/data.py][route_create_forum_post] Post créé par user {current_user_id}")
        return jsonify(post), 201

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_create_forum_post] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_create_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@forum_bp.route("/", methods=["GET"])
@jwt_required()
def route_get_all_forum_posts():
    """Retrieve all forum posts sorted by date or popularity."""
    try:
        sort_by = request.args.get("sort_by", "recent")
        posts = forum_service.get_all_forum_posts(sort_by)
        app.logger.info(f"[BACK][routes/data.py][route_get_all_forum_posts] {len(posts)} posts récupérés (sort_by={sort_by})")
        return jsonify(posts), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_get_all_forum_posts] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@forum_bp.route("/<post_id>", methods=["GET"])
@jwt_required()
def route_get_forum_post_by_id(post_id):
    """Retrieve a specific forum post with its comments."""
    try:
        post = forum_service.get_forum_post_by_id(post_id)
        app.logger.info(f"[BACK][routes/data.py][route_get_forum_post_by_id] Post {post_id} récupéré")
        return jsonify(post), 200

    except LookupError as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_get_forum_post_by_id] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_get_forum_post_by_id] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@forum_bp.route("/<post_id>", methods=["PUT"])
@jwt_required()
def route_update_forum_post(post_id):
    """Update a forum post — author only."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        updated_post = forum_service.update_forum_post_entry(post_id, data, current_user_id)
        app.logger.info(f"[BACK][routes/data.py][route_update_forum_post] Post {post_id} mis à jour par user {current_user_id}")
        return jsonify(updated_post), 200

    except LookupError as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_update_forum_post] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        app.logger.warning(f"[BACK][routes/forum_routes.py][route_update_forum_post] Accès refusé : {e}")
        return jsonify({"error": str(e)}), 403
    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_update_forum_post] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_update_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@forum_bp.route("/<post_id>", methods=["DELETE"])
@jwt_required()
def route_delete_forum_post(post_id):
    """Delete a forum post — author only."""
    try:
        current_user_id = get_jwt_identity()
        result = forum_service.delete_forum_post(post_id, current_user_id)
        app.logger.info(f"[BACK][routes/data.py][route_delete_forum_post] Post {post_id} supprimé par user {current_user_id}")
        return jsonify(result), 204

    except LookupError as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_delete_forum_post] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        app.logger.warning(f"[BACK][routes/forum_routes.py][route_delete_forum_post] Accès refusé : {e}")
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_delete_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@forum_bp.route("/<post_id>/like", methods=["POST"])
@jwt_required()
def route_toggle_like_forum_post(post_id):
    """Toggle a like on a forum post."""
    try:
        current_user_id = get_jwt_identity()
        result = forum_service.toggle_like_forum_post(post_id, current_user_id)
        app.logger.info(f"[BACK][routes/data.py][route_toggle_like_forum_post] User {current_user_id} → {result['message']} sur post {post_id}")
        return jsonify(result), 200

    except LookupError as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_toggle_like_forum_post] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        app.logger.warning(f"[BACK][routes/forum_routes.py][route_toggle_like_forum_post] Accès refusé : {e}")
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        app.logger.error(f"[BACK][routes/forum_routes.py][route_toggle_like_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
