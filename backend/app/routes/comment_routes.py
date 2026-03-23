"""
[BACK][routes/comment_routes.py]

Blueprint : comment_bp — prefix /forum/posts/<post_id>/comments
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /                       Create a comment on a post
  GET    /                       Retrieve all comments for a post
  PUT    /<comment_id>           Update a comment (author only)
  DELETE /<comment_id>           Delete a comment (author only)
  POST   /<comment_id>/like      Toggle like on a comment

HTTP status codes:
  201  Resource created
  200  Success (read / update / like)
  204  Success (delete, no content)
  400  Missing or malformed data
  401  Missing or invalid token
  403  Authenticated but forbidden (not author or own comment)
  404  Resource not found
  422  Data present but invalid (wrong type or format)
  500  Unexpected server error
"""


from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import comment_service

comment_bp = Blueprint('comment', __name__, url_prefix='/forum/posts/<post_id>/comments')


@comment_bp.route("/", methods=["POST"])
@jwt_required()
def route_create_comment(post_id):
    """Create a comment on a forum post."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            app.logger.error("[BACK][routes/data.py][route_create_comment] Requête vide ou invalide")
            return jsonify({"error": "Missing request body"}), 400

        comment = comment_service.create_comment_entry(post_id, current_user_id, data)
        app.logger.info(f"[BACK][routes/data.py][route_create_comment] Commentaire créé sur post {post_id} par user {current_user_id}")
        return jsonify(comment), 201

    except LookupError as e:
        app.logger.error(f"[BACK][routes/comment_routes.py][route_create_comment] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/comment_routes.py][route_create_comment] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_create_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/", methods=["GET"])
@jwt_required()
def route_get_comments_by_post(post_id):
    """Retrieve all comments for a given post."""
    try:
        comments = comment_service.get_comments_by_post(post_id)
        app.logger.info(f"[BACK][routes/comment_routes.py][route_get_comments_by_post] {len(comments)} commentaires récupérés pour le post {post_id}")
        return jsonify(comments), 200

    except LookupError as e:
        app.logger.error(f"[BACK][routes/comment_routes.py][route_get_comments_by_post] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_comments_by_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/<comment_id>", methods=["PUT"])
@jwt_required()
def route_update_comment(post_id, comment_id):
    """Update a comment — author only."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if not data:
            app.logger.error("[BACK][routes/data.py][route_update_comment] Aucune donnée reçue pour la mise à jour")
            return jsonify({"error": "Missing request body"}), 400

        updated_comment = comment_service.update_comment_entry(comment_id, current_user_id, data)
        app.logger.info(f"[BACK][routes/data.py][route_update_comment] Commentaire {comment_id} mis à jour par user {current_user_id}")
        return jsonify(updated_comment), 200

    except LookupError as e:
        app.logger.error(f"[BACK][routes/comment_routes.py][route_update_comment] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        app.logger.warning(f"[BACK][routes/comment_routes.py][route_update_comment] Accès refusé : {e}")
        return jsonify({"error": str(e)}), 403
    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/comment_routes.py][route_update_comment] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_update_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/<comment_id>", methods=["DELETE"])
@jwt_required()
def route_delete_comment(post_id, comment_id):
    """Delete a comment — author only."""
    try:
        current_user_id = get_jwt_identity()
        result = comment_service.delete_comment_entry(comment_id, current_user_id)
        app.logger.info(f"[BACK][routes/data.py][route_delete_comment] Commentaire {comment_id} supprimé par user {current_user_id}")
        return jsonify(result), 204

    except LookupError as e:
        app.logger.error(f"[BACK][routes/comment_routes.py][route_delete_comment] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        app.logger.warning(f"[BACK][routes/comment_routes.py][route_delete_comment] Accès refusé : {e}")
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_delete_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/<comment_id>/like", methods=["POST"])
@jwt_required()
def route_toggle_like_comment(post_id, comment_id):
    """Toggle a like on a comment."""
    try:
        current_user_id = get_jwt_identity()
        result = comment_service.toggle_like_comment(comment_id, current_user_id)
        app.logger.info(f"[BACK][routes/data.py][route_toggle_like_comment] User {current_user_id} → {result['message']} sur commentaire {comment_id}")
        return jsonify(result), 200

    except LookupError as e:
        app.logger.error(f"[BACK][routes/comment_routes.py][route_toggle_like_comment] Ressource introuvable : {e}")
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        app.logger.warning(f"[BACK][routes/comment_routes.py][route_toggle_like_comment] Accès refusé : {e}")
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_toggle_like_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500
