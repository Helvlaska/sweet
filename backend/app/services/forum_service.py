from flask import current_app as app
from app import db
from app.models import ForumPost, User


def validate_forum_post_data(data: dict):
    try:
        if not data:
            app.logger.error("[BACK][services/data_service.py][validate_forum_post_data] Aucune donnée reçue.")
            raise ValueError("Aucune donnée reçue pour la création du post sur le forum.")
        if "title" not in data or "content" not in data :
            app.logger.error("[BACK][services/data_service.py][validate_forum_post_data] Champs 'title' et 'content' requis.")
            raise ValueError("Les champs 'title' et 'content' sont requis")
        forum_post = ForumPost()
        forum_post.title = data.get("title")
        forum_post.content = data.get("content")
        app.logger.info(f"[BACK][services/data_service.py][validate_forum_post_data] Le titre: {forum_post.title}, le contenu: {forum_post.content} et son nombre de likes: {forum_post.likes} du post sont valides")
        return forum_post

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_forum_post_data] Erreur de validation des données du post : {str(e)}")
        raise


def create_forum_post_entry(user_id: str, data: dict):
    """Crée un nouveau post dans le forum."""
    try:
        forum_post = validate_forum_post_data(data)
        forum_post.user_id = user_id
        forum_post.save()
        app.logger.info(f"[BACK][services/data_service.py][create_forum_post_entry] Post {forum_post.title} créé par user {user_id}")
        return forum_post.to_dict()

    except (ValueError, TypeError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_forum_post_entry] Erreur lors de la création du post sur le forum : {e}")
        raise


def get_all_forum_posts(sort_by="recent"):
    """Retourne tous les posts triés par date ou popularité."""
    try:
        if sort_by == "popular":
            posts = ForumPost.query.order_by(ForumPost._likes.desc(), ForumPost.created_at.desc()).all() # type: ignore
        else:
            posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
        result = []
        for post in posts:
            posts_dict = post.to_dict()
            result.append(posts_dict)
        app.logger.info("[BACK][services/data_service.py][get_all_forum_posts] Liste des posts renvoyée")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_all_forum_posts] Erreur inattendue : {e}")
        raise


def get_forum_post_by_id(post_id: str):
    """Retourne un post et ses commentaires."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][get_forum_post_by_id] Post {post_id} introuvable")
            return None
        post_data = post.to_dict()
        post_data["comments"] = []
        for comment in post.comments:
            comment_dict = comment.to_dict()
            post_data["comments"].append(comment_dict)
            app.logger.info(f"[BACK][services/data_service.py][get_forum_post_by_id] Commentaire ajouté → {comment_dict.get('id')}")
        app.logger.info(f"[BACK][services/data_service.py][get_forum_post_by_id] Post {post_id} récupéré avec ses commentaires")
        return post_data

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_forum_post_by_id] Erreur inattendue : {e}")
        raise


def update_forum_post_entry(post_id: str, new_data: dict, user_id: str):
    """Modifie un post existant (seulement par son auteur)."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.info("[BACK][services/data_service.py][update_forum_post_entry] Aucune entrée trouvée pour cet utilisateur.")
            return None
        if post.user_id != user_id:
            app.logger.info("[BACK][services/data_service.py][update_forum_post_entry] Utilisateur non autorisé à modifier ce post")
            return None
        if "title" in new_data:
            validated_title = validate_forum_post_data({"title": new_data["title"], "content": post.content})
            post.title = validated_title.title
        if "content" in new_data:
            validated_content = validate_forum_post_data({"content": new_data["content"], "title": post.title})
            post.content = validated_content.content
        post.save()
        app.logger.info(f"[BACK][services/data_service.py][update_forum_post_entry] Post {post.id} mis à jour par user {user_id}")
        return post.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_forum_post_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_forum_post_entry] Erreur inattendue : {e}")
        raise


def delete_forum_post(post_id: str, user_id: str):
    """Supprime un post (auteur uniquement)."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.info(f"[BACK][services/data_service.py][delete_forum_post] Aucune entrée trouvée pour user {user_id} (entry_id: {post_id})")
            return None
        if post.user_id != user_id:
            app.logger.info("[BACK][services/data_service.py][delete_forum_post] Utilisateur non autorisé à supprimer ce post")
            return None
        post.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_forum_post] Post {post_id} supprimé par user {user_id}")
        return {"deleted_forum_post_id": post_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_forum_post] Erreur inattendue : {e}")
        raise


def toggle_like_forum_post(post_id: str, user_id: str):
    """Ajoute ou retire un like sur un post."""
    try:
        user = User.query.get(user_id)
        if not user:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_forum_post()] Utilisateur {user_id} introuvable")
            return None
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_forum_post()] Post {post_id} introuvable")
            return None
        if post.user_id == user_id:
            app.logger.info(f"[BACK][services/data_service.py][toggle_like_forum_post()] User {user_id} a tenté de liker son propre post {post_id}")
            return None
        if post in user.liked_posts:
            user.liked_posts.remove(post)
            post.likes -= 1
            message = "Like retiré"
        else:
            user.liked_posts.append(post)
            post.increment_likes()
            message = "Post liké"
        db.session.commit()
        app.logger.info(f"[BACK][services/data_service.py][toggle_like_forum_post()] User {user_id} → {message} post {post_id}")
        return {"post_id": post_id, "likes": post.likes, "message": message}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][toggle_like_forum_post()] Erreur inattendue : {e}")
        raise
