from flask import current_app as app
from app.models.base import BaseModel
from app.utils.validators import FORUM_CONTENT_PATTERN, FORUM_TITLE_PATTERN, is_valid
from app import db

class ForumPost(BaseModel):
    __tablename__ = "forum_posts"

    _title = db.Column(db.String(150), nullable=False)
    _content = db.Column(db.Text, nullable=False)
    _likes = db.Column(db.Integer, default=0, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship("Comment", backref="forum_posts", cascade="all, delete-orphan")


    @property
    def title(self):
        """Titre du post"""
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/forum_post.py][title.setter] Title n'est pas une string")
            raise TypeError("Le titre doit être une chaîne de caractères")
        cleaned_value = value.strip()
        if not cleaned_value:
            app.logger.error("[BACK][models/forum_post.py][title.setter] Title vide")
            raise ValueError("Le titre ne peut pas être vide")
        if not is_valid(cleaned_value, FORUM_TITLE_PATTERN):
            app.logger.error("[BACK][models/forum_post.py][title.setter] Format du titre invalide")
            raise ValueError("Le titre ne respecte pas le format attendu")
        app.logger.info("[BACK][models/forum_post.py][title.setter] Titre validé")
        self._title = cleaned_value


    @property
    def content(self):
        """Contenu du post"""
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/forum_post.py][content.setter] Content n'est pas une string")
            raise TypeError("Le contenu doit être une chaîne de caractères")
        cleaned_value = value.strip()
        if not cleaned_value:
            app.logger.error("[BACK][models/forum_post.py][content.setter] Content vide")
            raise ValueError("Le contenu ne peut pas être vide")
        if not is_valid(cleaned_value, FORUM_CONTENT_PATTERN):
            app.logger.error("[BACK][models/forum_post.py][content.setter] Format du contenu invalide")
            raise ValueError("Le contenu ne respecte pas le format attendu")
        app.logger.info("[BACK][models/forum_post.py][content.setter] Contenu validé")
        self._content = cleaned_value


    @property
    def likes(self):
        """Nombre de likes"""
        return self._likes

    @likes.setter
    def likes(self, value):
        if not isinstance(value, int):
            app.logger.error("[BACK][models/forum_post.py][likes.setter] Le nombre de likes doit être un entier")
            raise TypeError("Le nombre de likes doit être un entier")
        if value < 0:
            app.logger.error("[BACK][models/forum_post.py][likes.setter] Le nombre de likes ne peut pas être négatif")
            raise ValueError("Le nombre de likes ne peut pas être négatif")
        app.logger.info("[BACK][models/forum_post.py][likes.setter] Nombre de likes validé")
        self._likes = value
