from flask import current_app as app
from app import db
from app.models import Article, User

def validate_article_data(data: dict):
    """Validate and return an Article instance"""
    try:
        article = Article()
        article.title = data.get("title")
        article.content = data.get("content")
        article.likes = data.get("likes")
        app.logger.info(f"[BACK][services/article_service][validate_article_data] Données de l'article {article.title} validées")
        return article

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/article_service][validate_article_data] Erreur de validation : {str(e)}")
        raise


def create_article_entry(data: dict, user_id: str):
    """Create a new article (admin only)"""
    try:
        user = User.query.get(user_id)
        if not user:
            app.logger.error(f"[BACK][services/article_service][create_article_entry] User {user_id} introuvable")
            return None
        if user.role != "admin":
            app.logger.warning(f"[BACK][services/article_service][create_article_entry] User {user_id} non autorisé à créer un article")
            return None
        article = validate_article_data(data)
        article.user_id = user_id
        article.save()
        app.logger.info(f"[BACK][services/article_service][create_article_entry] Article {article.title} créé par admin {user_id}")
        return article.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/article_service][create_article_entry] Erreur inattendue : {e}")
        raise


def get_all_articles(sort_by: str = "recent"):
    """Retrieve all articles sorted by date or popularity"""
    try:
        if sort_by == "popular":
            articles = Article.query.order_by(Article._likes.desc(), Article.created_at.desc()).all() #type: ignore
        else:
            articles = Article.query.order_by(Article.created_at.desc()).all()
        result = []
        for article in articles:
            article_dict = article.to_dict()
            result.append(article_dict)
            app.logger.debug(f"[BACK][services/article_service][get_all_articles] Article ajouté → {article_dict.get('id')}")
        app.logger.info(f"[BACK][services/article_service][get_all_articles] {len(result)} articles récupérés (tri={sort_by})")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/article_service][get_all_articles] Erreur inattendue : {e}")
        raise


def get_article_by_id(article_id: str):
    """Retrieve a specific article by its ID"""
    try:
        article = Article.query.get(article_id)
        if not article:
            app.logger.error(f"[BACK][services/article_service][get_article_by_id] Article {article_id} introuvable")
            return None
        app.logger.info(f"[BACK][services/article_service][get_article_by_id] Article {article_id} récupéré")
        return article.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/article_service][get_article_by_id] Erreur inattendue : {e}")
        raise


def update_article_entry(article_id: str, user_id: str, data: dict):
    """Update an existing article (admin only)"""
    try:
        user = User.query.get(user_id)
        article = Article.query.get(article_id)
        if not article:
            app.logger.error(f"[BACK][services/article_service][update_article_entry] Article {article_id} introuvable")
            return None
        if not user or user.role != "admin":
            app.logger.warning(f"[BACK][services/article_service][update_article_entry] User {user_id} non autorisé à modifier un article")
            return None
        validated_article = validate_article_data(data)
        article.title = validated_article.title
        article.content = validated_article.content
        article.save()
        app.logger.info(f"[BACK][services/article_service][update_article_entry] Article {article.id} mis à jour par admin {user_id}")
        return article.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/article_service][update_article_entry] Erreur inattendue : {e}")
        raise


def delete_article_entry(article_id: str, user_id: str):
    """Delete an article (admin only)"""
    try:
        user = User.query.get(user_id)
        article = Article.query.get(article_id)
        if not article:
            app.logger.error(f"[BACK][services/article_service][delete_article_entry] Article {article_id} introuvable")
            return None
        if not user or user.role != "admin":
            app.logger.warning(f"[BACK][services/article_service][delete_article_entry] User {user_id} non autorisé à supprimer un article")
            return None
        article.delete()
        app.logger.info(f"[BACK][services/article_service][delete_article_entry] Article {article_id} supprimé par admin {user_id}")
        return {"deleted_article_id": article_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/article_service][delete_article_entry] Erreur inattendue : {e}")
        raise


def toggle_like_article(article_id: str, user_id: str):
    """Toggle a like on an article for the current user"""
    try:
        user = User.query.get(user_id)
        article = Article.query.get(article_id)
        if not user:
            app.logger.error(f"[BACK][services/article_service][toggle_like_article] Utilisateur {user_id} introuvable")
            return None
        if not article:
            app.logger.error(f"[BACK][services/article_service][toggle_like_article] Article {article_id} introuvable")
            return None
        if article.user_id == user_id:
            app.logger.info(f"[BACK][services/article_service][toggle_like_article] User {user_id} a tenté de liker son propre article {article_id}")
            return None
        if article in user.liked_articles:
            user.liked_articles.remove(article)
            article.likes -= 1
            message = "Like retiré"
        else:
            user.liked_articles.append(article)
            article.increment_likes()
            message = "Article liké"
        db.session.commit()
        app.logger.info(f"[BACK][services/article_service][toggle_like_article] User {user_id} → {message} sur article {article_id}")
        return {"article_id": article_id, "likes": article.likes, "message": message}

    except Exception as e:
        app.logger.error(f"[BACK][services/article_service][toggle_like_article] Erreur inattendue : {e}")
        raise
