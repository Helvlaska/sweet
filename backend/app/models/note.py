from flask import current_app as app
from app.models.base import BaseModel
from app import db

class Note(BaseModel):
    __tablename__ = "notes"

    _title = db.Column(db.String(80), nullable=False)
    _content = db.Column(db.String(1000), nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    health_professional_id = db.Column(db.String(36), db.ForeignKey("health_professionals.id", ondelete="SET NULL"), nullable=True)


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/note.py][title.setter] Le titre doit être une chaîne de caractères")
            raise TypeError("Le titre doit être une chaîne de caractères")
        cleaned_title = value.strip()
        if not (3 <= len(cleaned_title) <= 80):
            app.logger.error("[BACK][models/note.py][title.setter] Le titre doit comporter entre 3 et 80 caractères")
            raise ValueError("Le titre doit comporter entre 3 et 80 caractères")
        app.logger.info("[BACK][models/note.py][title.setter] Le titre est validé")
        self._title = cleaned_title


    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/note.py][content.setter] Le contenu doit être une chaîne de caractères")
            raise TypeError("Le contenu doit être une chaîne de caractères")
        cleaned_content = value.strip()
        if not (10 <= len(cleaned_content) <= 1000):
            app.logger.error("[BACK][models/note.py][content.setter] Le contenu doit comporter entre 10 et 1000 caractères")
            raise ValueError("Le contenu doit comporter entre 10 et 1000 caractères")
        app.logger.info("[BACK][models/note.py][content.setter] Le contenu est validé")
        self._content = cleaned_content
