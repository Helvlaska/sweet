from flask import current_app as app
from app.models.base import BaseModel
from app import db

class Glycemia(BaseModel):
    __tablename__ = "glycemias"

    UNIT = "mg/dl"
    _glucose_level = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    @property
    def glucose_level(self):
        return self._glucose_level

    @glucose_level.setter
    def glucose_level(self, value):
        if not isinstance(value, int):
            app.logger.error("[BACK][models/glycemia.py][glucose_level.setter] La glycémie doit être un integer")
            raise TypeError(f"La glycémie {value} doit être un nombre entier")
        if value < 50 or value > 350:
            app.logger.error(f"[BACK][models/glycemia.py][glucose_level.setter] La glycémie {value} doit se situer entre 50 et 350")
            raise ValueError("La glycémie doit se situer entre 50 et 350")
        app.logger.info(f"La mesure {value} de glycémie est valide")
        self._glucose_level = value
