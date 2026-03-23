"""
[BACK][models/comment.py]

Comment model — inherits from BaseModel (id, created_at, updated_at, entry_date, CRUD).

Fields:
  content   String (300), validated against COMMENT_CONTENT_PATTERN
  likes     Integer, non-negative (default 0)
  user_id   Foreign key → users.id
  post_id   Foreign key → forum_posts.id

All fields are exposed via validated property setters.
Write operations (create, update, delete) are restricted to the comment author.
"""


from flask import current_app as app
from app.models.base import BaseModel
from app.utils.validators import COMMENT_CONTENT_PATTERN, is_valid
from app import db


class Comment(BaseModel):
    __tablename__ = "comments"

    _content = db.Column(db.String(300), nullable=False)
    _likes = db.Column(db.Integer, default=0, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey("forum_posts.id"), nullable=False)


    @property
    def content(self):
        """Texte du commentaire"""
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/comment.py][content.setter] Content n'est pas une string")
            raise TypeError("Le contenu du commentaire doit être une chaîne de caractères")

        cleaned_value = value.strip()
        if not cleaned_value:
            app.logger.error("[BACK][models/comment.py][content.setter] Content vide")
            raise ValueError("Le commentaire ne peut pas être vide")

        if not is_valid(cleaned_value, COMMENT_CONTENT_PATTERN):
            app.logger.error("[BACK][models/comment.py][content.setter] Format du contenu invalide")
            raise ValueError("Le commentaire ne respecte pas le format attendu (max 300 caractères)")

        app.logger.info("[BACK][models/comment.py][content.setter] Contenu validé")
        self._content = cleaned_value


    @property
    def likes(self):
        """Nombre de likes du commentaire"""
        return self._likes

    @likes.setter
    def likes(self, value):
        if not isinstance(value, int):
            app.logger.error("[BACK][models/comment.py][likes.setter] Likes doit être un entier")
            raise TypeError("Le nombre de likes doit être un entier")

        if value < 0:
            app.logger.error("[BACK][models/comment.py][likes.setter] Likes ne peut pas être négatif")
            raise ValueError("Le nombre de likes ne peut pas être négatif")

        app.logger.info("[BACK][models/comment.py][likes.setter] Nombre de likes validé")
        self._likes = value
