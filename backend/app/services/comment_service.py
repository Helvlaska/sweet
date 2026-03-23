"""
[BACK][services/comment_service.py]

Service layer — comment business logic.
Called exclusively from comment_routes.py.

Exposed functions:
  validate_comment_data(data)
  create_comment_entry(post_id, user_id, data)
  get_comments_by_post(post_id)
  update_comment_entry(comment_id, user_id, data)
  delete_comment_entry(comment_id, user_id)
  toggle_like_comment(comment_id, user_id)

Access control:
  create    → any authenticated user
  read      → public
  update, delete → author only
  like      → any authenticated user except comment author
"""


from flask import current_app as app
from app import db
from app.models import Comment, ForumPost, User


def validate_comment_data(data: dict) -> Comment:
    """Validate and return a Comment instance"""
    try:
        comment = Comment()
        comment.content = data.get("content")
        app.logger.info(f"[BACK][services/data_service.py][validate_comment_data] Le contenu {comment.content} et les likes {comment.likes} du commentaire sont valides")
        return comment

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_comment_data] Erreur de validation du commentaire: {str(e)}")
        raise


def create_comment_entry(post_id: str, user_id: str, data: dict) -> Comment:
    """Create a new comment on a forum post. Raises LookupError if post not found."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][create_comment_entry] Post {post_id} introuvable")
            raise LookupError(f"Post {post_id} not found")

        validated_comment = validate_comment_data(data)
        validated_comment.user_id = user_id
        validated_comment.post_id = post_id
        validated_comment.save()
        app.logger.info(f"[BACK][services/data_service.py][create_comment_entry] Commentaire {validated_comment.id} créé sur post {post_id} par user {user_id}")
        return validated_comment.to_dict()  # type: ignore

    except (ValueError, TypeError, LookupError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_comment_entry] Erreur inattendue : {e}")
        raise


def get_comments_by_post(post_id: str):
    """Retrieve all comments for a given post. Raises LookupError if post not found."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][get_comments_by_post] Post {post_id} introuvable")
            raise LookupError(f"Post {post_id} not found")

        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
        result = []

        for comment in comments:
            comment_dict = comment.to_dict()
            result.append(comment_dict)
            app.logger.debug(f"[BACK][services/data_service.py][get_comments_by_post] Commentaire ajouté → {comment_dict.get('id')}")

        app.logger.info(f"[BACK][services/data_service.py][get_comments_by_post] {len(result)} commentaires récupérés pour le post {post_id}")
        return result

    except LookupError:
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_comments_by_post] Erreur inattendue : {e}")
        raise


def update_comment_entry(comment_id: str, user_id: str, data: dict):
    """Update a comment — author only. Raises LookupError if not found, PermissionError if not author."""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][update_comment_entry] Commentaire {comment_id} introuvable")
            raise LookupError(f"Comment {comment_id} not found")
        if comment.user_id != user_id:
            app.logger.info(f"[BACK][services/data_service.py][update_comment_entry] User {user_id} non autorisé à modifier ce commentaire")
            raise PermissionError("Only the author can update this comment")
        validated_comment = validate_comment_data(data)
        comment.content = validated_comment.content
        comment.save()
        app.logger.info(f"[BACK][services/data_service.py][update_comment_entry] Commentaire {comment.id} mis à jour par user {user_id}")
        return comment.to_dict()

    except (ValueError, TypeError, LookupError, PermissionError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_comment_entry] Erreur inattendue : {e}")
        raise


def delete_comment_entry(comment_id: str, user_id: str):
    """Delete a comment — author only. Raises LookupError if not found, PermissionError if not author."""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][delete_comment_entry] Commentaire {comment_id} introuvable")
            raise LookupError(f"Comment {comment_id} not found")

        if comment.user_id != user_id:
            app.logger.info(f"[BACK][services/data_service.py][delete_comment_entry] User {user_id} non autorisé à supprimer ce commentaire")
            raise PermissionError("Only the author can delete this comment")

        comment.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_comment_entry] Commentaire {comment_id} supprimé par user {user_id}")
        return {"deleted_comment_id": comment_id}

    except (LookupError, PermissionError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_comment_entry] Erreur inattendue : {e}")
        raise


def toggle_like_comment(comment_id: str, user_id: str):
    """Toggle a like on a comment. Raises LookupError if not found, PermissionError if own comment."""
    try:
        user = User.query.get(user_id)
        if not user:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Utilisateur {user_id} introuvable")
            raise LookupError(f"User {user_id} not found")

        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Commentaire {comment_id} introuvable")
            raise LookupError(f"Comment {comment_id} not found")

        if comment.user_id == user_id:
            app.logger.info(f"[BACK][services/data_service.py][toggle_like_comment] User {user_id} a tenté de liker son propre commentaire {comment_id}")
            raise PermissionError("Cannot like your own comment")

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

    except (LookupError, PermissionError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Erreur inattendue : {e}")
        raise
