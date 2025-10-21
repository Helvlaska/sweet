from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import article_service

article_bp = Blueprint('article', __name__, url_prefix='/article')

@article_bp.route("/", methods=["POST"])
@jwt_required()
def create_article_route():
    """Create a new article (admin only)"""
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        new_article = article_service.create_article_entry(admin_id, data)
        if not new_article:
            return jsonify({"error": "Création de l'article impossible"}), 403
        app.logger.info(f"[BACK][routes/article_routes][create_article_route] Article {new_article} créé par l'admin {admin_id}")
        return jsonify(new_article), 201

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/article_routes][create_article_route] Données de l'article NOK: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/article_routes][create_article_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@article_bp.route("/", methods=["GET"])
def get_all_articles_route():
    """Retrieve all articles sorted by date or popularity"""
    try:
        sort_by = request.args.get("sort_by", "recent")
        articles = article_service.get_all_articles(sort_by)
        if articles is None or len(articles) == 0:
            app.logger.error("[BACK][routes/article_routes][route_get_all_articles] Aucun article trouvé")
            return jsonify({"message": "Article not found"}), 200
        app.logger.info(f"[BACK][routes/article_routes][route_get_all_articles] {len(articles)} articles récupérés (sort_by={sort_by})")
        return jsonify(articles), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/article_routes][get_activity_entry_route] Erreur Date ou Timelaps: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/article_routes][get_activity_entry_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@article_bp.route("/<article_id>", methods=["GET"])
def get_article_by_id_route(article_id):
    """Retrieve a specific article by its ID"""
    try:
        article = article_service.get_article_by_id(article_id)
        if not article:
            app.logger.error("[BACK][routes/article_routes][route_get_article_by_id] L'article est introuvable")
            return jsonify({"error": "Article not found"}), 404
        app.logger.info(f"[BACK][routes/article_routes][route_get_article_by_id] Article {article_id} récupéré")
        return jsonify(article), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/article_routes][get_article_by_id_route] Erreur sur les valeurs entrées: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/article_routes][get_article_by_id_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@article_bp.route("/<article_id>", methods=["PUT"])
@jwt_required()
def update_article_route(article_id):
    """Update an existing article (admin only)"""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        if not new_data:
            app.logger.error("[BACK][routes/article_routes][update_article_route] Aucune donnée reçue")
            return jsonify({"error": "Missing JSON data"}), 400
        updated_article = article_service.update_article_entry(article_id, user_id, new_data)
        if not updated_article:
            app.logger.error("[BACK][routes/article_routes][update_article_route] Article non trouvé")
            return jsonify({"error": "Article not found"}), 404
        app.logger.info(f"[BACK][routes/article_routes][update_article_route] Article {article_id} mis à jour par l'admin {user_id}")
        return jsonify(updated_article), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/article_routes][update_article_route] Erreur sur les valeurs entrées: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/article_routes][update_article_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@article_bp.route("/<article_id>", methods=["DELETE"])
@jwt_required()
def delete_article_route(article_id):
    """Delete an article (admin only)"""
    try:
        user_id = get_jwt_identity()
        result = article_service.delete_article_entry(article_id, user_id)
        if not result:
            app.logger.error("[BACK][routes/article_routes][delete_article_route] Article non trouvé")
            return jsonify({"error": "Article not found"}), 404
        app.logger.info(f"[BACK][routes/article_routes][delete_article_route] Article {article_id} supprimé par admin {user_id}")
        return "", 204

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/article_routes][delete_article_route] Erreur sur les valeurs entrées: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/article_routes][delete_article_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500


@article_bp.route("/<article_id>/like", methods=["POST"])
@jwt_required()
def toggle_like_article_route(article_id):
    """Toggle a like on an article for the current user"""
    try:
        user_id = get_jwt_identity()
        result = article_service.toggle_like_article(article_id, user_id)
        if not result:
            app.logger.error("[BACK][routes/article_routes][toggle_like_article_route] Article non trouvé")
            return jsonify({"error": "Article not found"}), 404
        app.logger.info(f"[BACK][routes/article_routes][toggle_like_article_route] User {user_id} → {result['message']} sur article {article_id}")
        return jsonify(result), 200

    except ValueError as e:
        app.logger.warning(f"[BACK][routes/article_routes][toggle_like_article_route] Erreur sur les valeurs entrées: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"[BACK][routes/article_routes][toggle_like_article_route] Erreur: {e}")
        return jsonify({"error": "Internal server error"}), 500
