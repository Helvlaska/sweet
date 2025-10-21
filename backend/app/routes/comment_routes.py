from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import comment_service

comment_bp = Blueprint('comment', __name__, url_prefix='/forum/posts/<post_id>/comments')

@comment_bp.route("/", methods=["POST"])
@jwt_required()
def route_create_comment(post_id):
    """Crée un commentaire associé à un post."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error("[BACK][routes/data.py][route_create_comment] Requête vide ou invalide")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        comment = comment_service.create_comment_entry(post_id, current_user_id, data)
        if not comment:
            app.logger.error("[BACK][routes/data.py][route_create_comment] Échec de création du commentaire")
            return jsonify({"error": "Création du commentaire impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_create_comment] Commentaire créé sur post {post_id} par user {current_user_id}")
        return jsonify(comment), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_create_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/", methods=["GET"])
def route_get_comments_by_post(post_id):
    """Récupère tous les commentaires d’un post donné."""
    try:
        comments = comment_service.get_comments_by_post(post_id)
        if comments is None:
            app.logger.warning(f"[BACK][routes/data.py][route_get_comments_by_post] Aucun commentaire trouvé pour le post {post_id}")
            return jsonify({"message": "Aucun commentaire trouvé"}), 200
        for comment in comments:
            app.logger.debug(f"[BACK][routes/data.py][route_get_comments_by_post] Commentaire trouvé → {comment.get('id')}")
        app.logger.info(f"[BACK][routes/data.py][route_get_comments_by_post] {len(comments)} commentaires récupérés pour le post {post_id}")
        return jsonify(comments), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_comments_by_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/<comment_id>", methods=["PUT"])
@jwt_required()
def route_update_comment(comment_id):
    """Met à jour un commentaire (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error("[BACK][routes/data.py][route_update_comment] Aucune donnée reçue pour la mise à jour")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        updated_comment = comment_service.update_comment_entry(comment_id, current_user_id, data)
        if updated_comment is None:
            app.logger.error(f"[BACK][routes/data.py][route_update_comment] Mise à jour du commentaire {comment_id} impossible")
            return jsonify({"error": "Mise à jour impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_update_comment] Commentaire {comment_id} mis à jour par user {current_user_id}")
        return jsonify(updated_comment), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_update_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/<comment_id>", methods=["DELETE"])
@jwt_required()
def route_delete_comment(comment_id):
    """Supprime un commentaire (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        result = comment_service.delete_comment_entry(comment_id, current_user_id)
        if not result:
            app.logger.error(f"[BACK][routes/data.py][route_delete_comment] Suppression du commentaire {comment_id} impossible")
            return jsonify({"error": "Suppression impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_delete_comment] Commentaire {comment_id} supprimé par user {current_user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_delete_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/<comment_id>/like", methods=["POST"])
@jwt_required()
def route_toggle_like_comment(comment_id):
    """Ajoute ou retire un like sur un commentaire."""
    try:
        current_user_id = get_jwt_identity()
        result = comment_service.toggle_like_comment(comment_id, current_user_id)
        if not result:
            app.logger.error(f"[BACK][routes/data.py][route_toggle_like_comment] Action impossible pour le commentaire {comment_id}")
            return jsonify({"error": "Action impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_toggle_like_comment] User {current_user_id} → {result['message']} sur commentaire {comment_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_toggle_like_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500
