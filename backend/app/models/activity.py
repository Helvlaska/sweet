from flask import current_app as app
from app.models.base import BaseModel
from app import db

class Activity(BaseModel):
    __tablename__ = "activities"

    UNIT = "min/day"
    _description = db.Column(db.Enum("marche","natation","vélo","yoga", "pilates", "renforcement", "jardinage", "bricolage", "ménage", "escaliers"), nullable=False)
    _duration = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        allowed = {"marche","natation","vélo","yoga", "pilates", "renforcement", "jardinage", "bricolage", "ménage", "escaliers"}
        if not isinstance(value, str):
            app.logger.error(f"[BACK][models/activity.py][description.setter] La description doit être une chaine de caractère parmis cette liste: {allowed}")
            raise TypeError(f"La description doit être une chaine de caractères parmis cette liste: {allowed}")
        if value not in allowed:
            app.logger.error(f"[BACK][models/activity.py][description.setter] La description doit être parmis cette liste: {allowed}")
            raise ValueError(f"La description doit être parmis cette liste: {allowed}")
        app.logger.info(f"[BACK][models/activity.py][description.setter] La description {value} est validée")
        self._description = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if not isinstance(value, int):
            app.logger.error("[BACK][models/activity.py][duration.setter] La durée doit être un nombre entier")
            raise TypeError("[BACK][models/activity.py][duration.setter] La durée doit être un nombre entier")
        if value <= 0 or value > 600:
            app.logger.error("[BACK][models/activity.py][duration.setter] La durée doit se situer entre 1 et 600 minutes")
            raise ValueError("La durée doit être comprise entre 1 et 600 minutes (10 heures maximum)")
        app.logger.info(f"[BACK][models/activity.py][duration.setter] la durée {value} est valide")
        self._duration = value
