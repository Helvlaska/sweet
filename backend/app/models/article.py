from flask import current_app as app
from app.models.base import BaseModel
from app.utils.validators import ARTICLE_CONTENT_PATTERN, ARTICLE_TITLE_PATTERN, is_valid
from app import db

class Article(BaseModel):
    __tablename__ = "articles"

    _title = db.Column(db.String(200), nullable=False)
    _content = db.Column(db.Text, nullable=False)
    _likes = db.Column(db.Integer, default=0, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


    @property
    def title(self):
        """Titre de l'article"""
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/article.py][title.setter] Title n'est pas une string")
            raise TypeError("Le titre doit être une chaîne de caractères")
        cleaned_value = value.strip()
        if not cleaned_value:
            app.logger.error("[BACK][models/article.py][title.setter] Title vide")
            raise ValueError("Le titre ne peut pas être vide")
        if not is_valid(cleaned_value, ARTICLE_TITLE_PATTERN):
            app.logger.error("[BACK][models/article.py][title.setter] Format du titre invalide")
            raise ValueError("Le titre ne respecte pas le format attendu")
        app.logger.info("[BACK][models/article.py][title.setter] Titre validé")
        self._title = cleaned_value


    @property
    def content(self):
        """Contenu de l'article"""
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/article.py][content.setter] Content n'est pas une string")
            raise TypeError("Le contenu de l'article doit être une chaîne de caractères")
        cleaned_value = value.strip()
        if not cleaned_value:
            app.logger.error("[BACK][models/article.py][content.setter] Content vide")
            raise ValueError("Le contenu ne peut pas être vide")
        if not is_valid(cleaned_value, ARTICLE_CONTENT_PATTERN):
            app.logger.error("[BACK][models/article.py][content.setter] Format du contenu invalide")
            raise ValueError("Le contenu ne respecte pas le format attendu (min 20 caractères, max 50 000)")
        app.logger.info("[BACK][models/article.py][content.setter] Contenu validé")
        self._content = cleaned_value


    @property
    def likes(self):
        """Nombre de likes de l'article"""
        return self._likes

    @likes.setter
    def likes(self, value):
        if not isinstance(value, int):
            app.logger.error("[BACK][models/article.py][likes.setter] Likes doit être un entier")
            raise TypeError("Le nombre de likes doit être un entier")
        if value < 0:
            app.logger.error("[BACK][models/article.py][likes.setter] Likes ne peut pas être négatif")
            raise ValueError("Le nombre de likes ne peut pas être négatif")
        app.logger.info("[BACK][models/article.py][likes.setter] Nombre de likes validé")
        self._likes = value
