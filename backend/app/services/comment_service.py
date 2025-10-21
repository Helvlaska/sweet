from flask import current_app as app
from app.models import Comment


def validate_comment_data(data: dict) -> Comment:
    try:
        comment = Comment()
        comment.content = data.get("content")
        app.logger.info(f"[BACK][services/data_service.py][validate_comment_data] Le contenu {comment.content} et les likes {comment.likes} du commentaire sont valides")
        return comment

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_comment_data] Erreur de validation du commentaire: {str(e)}")
        raise


def create_comment_entry(post_id: str, user_id: str, data: dict) -> Comment:
    """Crée un nouveau commentaire associé à un post du forum."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][create_comment_entry] Post {post_id} introuvable")
            return None # type: ignore
        validated_comment = validate_comment_data(data)
        validated_comment.user_id = user_id
        validated_comment.post_id = post_id
        validated_comment.save()
        app.logger.info(f"[BACK][services/data_service.py][create_comment_entry] Commentaire {validated_comment.id} créé sur post {post_id} par user {user_id}")
        return validated_comment.to_dict() # type: ignore

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_comment_entry] Erreur inattendue : {e}")
        raise


def get_comments_by_post(post_id: str):
    """Récupère tous les commentaires d’un post."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][get_comments_by_post] Post {post_id} introuvable")
            return None
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
        result = []
        for comment in comments:
            comment_dict = comment.to_dict()
            result.append(comment_dict)
            app.logger.debug(f"[BACK][services/data_service.py][get_comments_by_post] Commentaire ajouté → {comment_dict.get('id')}")
        app.logger.info(f"[BACK][services/data_service.py][get_comments_by_post] {len(result)} commentaires récupérés pour le post {post_id}")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_comments_by_post] Erreur inattendue : {e}")
        raise


def update_comment_entry(comment_id: str, user_id: str, data: dict):
    """Modifie un commentaire existant (auteur uniquement)."""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][update_comment_entry] Commentaire {comment_id} introuvable")
            return None
        if comment.user_id != user_id:
            app.logger.info(f"[BACK][services/data_service.py][update_comment_entry] User {user_id} non autorisé à modifier ce commentaire")
            return None
        validated_comment = validate_comment_data(data)
        comment.content = validated_comment.content
        comment.save()
        app.logger.info(f"[BACK][services/data_service.py][update_comment_entry] Commentaire {comment.id} mis à jour par user {user_id}")
        return comment.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_comment_entry] Erreur inattendue : {e}")
        raise


def delete_comment_entry(comment_id: str, user_id: str):
    """Supprime un commentaire (auteur uniquement)."""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][delete_comment_entry] Commentaire {comment_id} introuvable")
            return None
        if comment.user_id != user_id:
            app.logger.info(f"[BACK][services/data_service.py][delete_comment_entry] User {user_id} non autorisé à supprimer ce commentaire")
            return None
        comment.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_comment_entry] Commentaire {comment_id} supprimé par user {user_id}")
        return {"deleted_comment_id": comment_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_comment_entry] Erreur inattendue : {e}")
        raise


def toggle_like_comment(comment_id: str, user_id: str):
    """Ajoute ou retire un like sur un commentaire (toggle)."""
    try:
        user = User.query.get(user_id)
        if not user:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Utilisateur {user_id} introuvable")
            return None
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Commentaire {comment_id} introuvable")
            return None
        if comment.user_id == user_id:
            app.logger.info(f"[BACK][services/data_service.py][toggle_like_comment] User {user_id} a tenté de liker son propre commentaire {comment_id}")
            return None
        if comment in user.liked_comments:
            user.liked_comments.remove(comment)
            comment.likes -= 1
            message = "Like retiré"
        else:
            user.liked_comments.append(comment)
            comment.increment_likes()
            message = "Commentaire liké"
        db.session.commit()
        app.logger.info(f"[BACK][services/data_service.py][toggle_like_comment] User {user_id} → {message} sur commentaire {comment_id}")
        return {"comment_id": comment_id, "likes": comment.likes, "message": message}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Erreur inattendue : {e}")
        raise
