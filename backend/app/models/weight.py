from flask import current_app as app
from app import db
from app.models.base import BaseModel

class Weight(BaseModel):
    __tablename__ = "weights"

    UNIT = "kg"
    _mass = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        if not isinstance(value, float):
            app.logger.error("[BACK][models/weight.py][mass.setter] Le poids doit être un float")
            raise TypeError("Le poids doit être un float")
        if value < 1.00 or value > 400.00:
            app.logger.error("[BACK][models/weight.py][mass.setter] Le poids doit être compris entre 1 et 400 kg")
            raise ValueError("Le poids doit être compris entre 1 et 400 kg")
        value = round(float, 2)
        self._mass = value
