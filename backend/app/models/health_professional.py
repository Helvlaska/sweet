from flask import current_app as app
from app.models.base import BaseModel
from app.utils.validators import PHONE_PATTERN, is_valid
from app import db

class HealthProfessional(BaseModel):
    __tablename__ = "health_professionals"


    SPECIALITY_CHOICES = ("general_practitioner", "diabetologist", "endocrinologist", "cardiologist", "ophthalmologist", "nephrologist", "podiatrist", "dentist", "dietitian", "nurse", "psychologist", "pharmacist", "physiotherapist", "physical_educator", "social_worker", "gynecologist")

    _fullname = db.Column(db.String(100), nullable=False)
    _speciality = db.Column(db.Enum(*SPECIALITY_CHOICES), nullable=False)
    _phone = db.Column(db.String(20), nullable=True)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    notes = db.relationship("Note", backref="health_professional", cascade="all, delete-orphan", lazy=True)



    @property
    def fullname(self):
        return self._fullname

    @fullname.setter
    def fullname(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/health_professional.py][fullname.setter] Le nom du professionnel doit être une chaîne de caractères")
            raise TypeError("Le nom du professionnel doit être une chaîne de caractères")
        cleaned_name = value.strip()
        if len(cleaned_name) < 2 or len(cleaned_name) > 100:
            app.logger.error("[BACK][models/health_professional.py][fullname.setter] Le nom doit comporter entre 2 et 100 caractères")
            raise ValueError("Le nom du professionnel doit comporter entre 2 et 100 caractères")
        app.logger.info("[BACK][models/health_professional.py][fullname.setter] Le nom du professionnel est validé")
        self._fullname = cleaned_name.title()


    @property
    def speciality(self):
        return self._speciality

    @speciality.setter
    def speciality(self, value):
        allowed = set(self.SPECIALITY_CHOICES)
        if not isinstance(value, str):
            app.logger.error(f"[BACK][models/health_professional.py][speciality.setter] La spécialité doit être une chaîne parmi : {allowed}")
            raise TypeError(f"La spécialité doit être une chaîne parmi : {allowed}")
        if value not in allowed:
            app.logger.error(f"[BACK][models/health_professional.py][speciality.setter] Spécialité non valide. Valeurs autorisées : {allowed}")
            raise ValueError(f"La spécialité doit être parmi : {allowed}")
        app.logger.info("[BACK][models/health_professional.py][speciality.setter] La spécialité est validée")
        self._speciality = value


    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        """Valide et formate le numéro de téléphone du professionnel de santé"""
        if value is None:
            self._phone = None
            return
        if not isinstance(value, str):
            app.logger.error("[BACK][models/health_professional.py][phone.setter] Le numéro doit être une chaîne de caractères.")
            raise TypeError("Le numéro de téléphone doit être une chaîne de caractères")
        cleaned_phone = value.strip()
        if not is_valid(cleaned_phone, PHONE_PATTERN):
            app.logger.error(f"[BACK][models/health_professional.py][phone.setter] Format invalide pour le numéro : {cleaned_phone}")
            raise ValueError("Le numéro de téléphone n’est pas valide")
        app.logger.info("[BACK][models/health_professional.py][phone.setter] Le numéro de téléphone est validé")
        self._phone = cleaned_phone
