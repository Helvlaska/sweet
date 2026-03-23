"""
[BACK][models/mood.py]

Mood model — inherits from BaseModel (id, created_at, updated_at, entry_date, CRUD).

Fields:
  description   Enum (Joyeux, Calme, Motivé, Fatigué, Anxieux, Irritable, Déprimé, Neutre)
  user_id       Foreign key → users.id

All fields are exposed via validated property setters.
"""


from flask import current_app as app
from app.models.base import BaseModel
from app import db


class Mood(BaseModel):
    __tablename__ = "moods"

    _description = db.Column(db.Enum("Joyeux", "Calme", "Motivé", "Fatigué", "Anxieux", "Irritable", "Déprimé", "Neutre"), nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)


    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        allowed = {"Joyeux", "Calme", "Motivé", "Fatigué", "Anxieux", "Irritable", "Déprimé", "Neutre"}
        if not isinstance(value, str):
            app.logger.error(f"[BACK][models/mood.py][description.setter] La description doit être une chaine de caractère parmis cette liste: {allowed}")
            raise TypeError(f"La description doit être une chaine de caractères parmis cette liste: {allowed}")

        if value not in allowed:
            app.logger.error(f"[BACK][models/mood.py][description.setter] La description doit être parmis cette liste: {allowed}")
            raise ValueError(f"La description doit être parmis cette liste: {allowed}")
        
        app.logger.info("[BACK][models/mood.py][description.setter] La description est validée")
        self._description = value
