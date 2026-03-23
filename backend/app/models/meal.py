"""
[BACK][models/meal.py]

Meal model — inherits from BaseModel (id, created_at, updated_at, entry_date, CRUD).

Fields:
  meal_type     Enum (breakfast, lunch, dinner, snack), required
  description   String (300), min 3 chars, required
  user_id       Foreign key → users.id

All fields are exposed via validated property setters.
"""


from flask import current_app as app
from app.models.base import BaseModel
from app import db


class Meal(BaseModel):
    __tablename__ = "meals"

    _meal_type = db.Column(db.Enum("breakfast", "lunch", "dinner", "snack"), nullable=False)
    _description = db.Column(db.String(300), nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)


    @property
    def meal_type(self):
        return self._meal_type

    @meal_type.setter
    def meal_type(self, value):
        allowed = {"breakfast", "lunch", "dinner", "snack"}
        if not isinstance(value, str):
            app.logger.error(f"[BACK][models/meal.py][meal_type.setter] Le type de repas doit être une chaine de caractère parmis cette liste: {allowed}")
            raise TypeError(f"Le type de repas doit être une chaine de caractères parmis cette liste: {allowed}")

        if value not in allowed:
            app.logger.error(f"[BACK][models/meal.py][meal_type.setter] Le type de repas doit être parmis cette liste: {allowed}")
            raise ValueError(f"Le type de repas doit être parmis cette liste: {allowed}")

        app.logger.info("[BACK][models/meal.py][meal_type.setter] Le type de repas est validé")
        self._meal_type = value


    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/meal.py][description.setter] Le champ description doit être une chaîne de caractères")
            raise TypeError("La description doit être une chaîne de caractères")

        cleaned_value = value.strip()
        if not cleaned_value:
            app.logger.error("[BACK][models/meal.py][description.setter] Le champ description est vide")
            raise ValueError("Le champ description ne peut pas être vide")

        if len(cleaned_value) < 3:
            app.logger.error("[BACK][models/meal.py][description.setter] Le champ description est trop court")
            raise ValueError("La description est trop courte (3 caractères minimum)")

        if len(cleaned_value) > 300:
            app.logger.error("[BACK][models/meal.py][description.setter] Le champ description dépasse la limite autorisée (300 caractères)")
            raise ValueError("La description ne doit pas dépasser 300 caractères")
        
        app.logger.info("[BACK][models/meal.py][description.setter] La description est validée")
        self._description = cleaned_value
