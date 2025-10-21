from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import forum_service

forum_bp = Blueprint('forum', __name__, url_prefix='/forum/posts')


@forum_bp.route("/", methods=["POST"])
@jwt_required()
def route_create_forum_post():
    """Crée un nouveau post de forum."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error("[BACK][routes/data.py][route_create_forum_post] Requête vide ou invalide")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        post = forum_service.create_forum_post_entry(current_user_id, data)
        if not post:
            return jsonify({"error": "Création du post impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_create_forum_post] Post créé par user {current_user_id}")
        return jsonify(post), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_create_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@forum_bp.route("/", methods=["GET"])
def route_get_all_forum_posts():
    """Récupère la liste complète des posts (tri date/popularité)."""
    try:
        sort_by = request.args.get("sort_by", "recent")
        posts = forum_service.get_all_forum_posts(sort_by)
        if posts is None or len(posts) == 0:
            return jsonify({"message": "Aucun post trouvé"}), 200
        app.logger.info(f"[BACK][routes/data.py][route_get_all_forum_posts] {len(posts)} posts récupérés (sort_by={sort_by})")
        return jsonify(posts), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_all_forum_posts] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@forum_bp.route("/<post_id>", methods=["GET"])
def route_get_forum_post_by_id(post_id):
    """Récupère un post précis avec ses commentaires."""
    try:
        post = forum_service.get_forum_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post introuvable"}), 404
        app.logger.info(f"[BACK][routes/data.py][route_get_forum_post_by_id] Post {post_id} récupéré")
        return jsonify(post), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_forum_post_by_id] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@forum_bp.route("/<post_id>", methods=["PUT"])
@jwt_required()
def route_update_forum_post(post_id):
    """Met à jour un post (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400
        updated_post = forum_service.update_forum_post_entry(post_id, data, current_user_id)
        if updated_post is None:
            return jsonify({"error": "Modification impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_update_forum_post] Post {post_id} mis à jour par user {current_user_id}")
        return jsonify(updated_post), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_update_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@forum_bp.route("/<post_id>", methods=["DELETE"])
@jwt_required()
def route_delete_forum_post(post_id):
    """Supprime un post (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        result = forum_service.delete_forum_post(post_id, current_user_id)
        if not result:
            return jsonify({"error": "Suppression impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_delete_forum_post] Post {post_id} supprimé par user {current_user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_delete_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@forum_bp.route("/<post_id>/like", methods=["POST"])
@jwt_required()
def route_toggle_like_forum_post(post_id):
    """Ajoute ou retire un like sur un post."""
    try:
        current_user_id = get_jwt_identity()
        result = forum_service.toggle_like_forum_post(post_id, current_user_id)
        if not result:
            return jsonify({"error": "Action impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_toggle_like_forum_post] User {current_user_id} → {result['message']} sur post {post_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_toggle_like_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500
