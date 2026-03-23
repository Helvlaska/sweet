"""
[BACK][models/health_professional.py]

HealthProfessional model — inherits from BaseModel (id, created_at, updated_at, entry_date, CRUD).

Fields:
  fullname      String (100), required, title-cased
  speciality    Enum (16 choices), required
  phone         String (20), optional, validated against PHONE_PATTERN
  email         String (254), optional, validated against EMAIL_PATTERN
  address       String (120), optional
  postal_code   String (10), optional
  city          String (120), optional, validated against CITY_PATTERN
  user_id       Foreign key → users.id

Relationships:
  notes      → Note (lazy)
  documents  → HealthDocument (lazy)

to_dict() is overridden to include serialized notes and documents.
"""


from flask import current_app as app
from app.models.base import BaseModel
from app.utils.validators import PHONE_PATTERN, EMAIL_PATTERN, CITY_PATTERN, is_valid
from app import db


class HealthProfessional(BaseModel):
    __tablename__ = "health_professionals"

    SPECIALITY_CHOICES = (
        "general_practitioner",
        "diabetologist",
        "endocrinologist",
        "cardiologist",
        "ophthalmologist",
        "nephrologist",
        "podiatrist",
        "dentist",
        "dietitian",
        "nurse",
        "psychologist",
        "pharmacist",
        "physiotherapist",
        "physical_educator",
        "social_worker",
        "gynecologist"
    )

    _fullname = db.Column(db.String(100), nullable=False)
    _speciality = db.Column(db.Enum(*SPECIALITY_CHOICES), nullable=False)
    _phone = db.Column(db.String(20), nullable=True)
    _email = db.Column(db.String(254), nullable=True)
    _address = db.Column(db.String(120), nullable=True)
    _postal_code = db.Column(db.String(10), nullable=True)
    _city = db.Column(db.String(120), nullable=True)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    notes = db.relationship("Note", backref="health_professional", lazy=True)
    documents = db.relationship("HealthDocument", backref="health_professional", lazy=True)



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


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            self._email = None
            return

        if not isinstance(value, str):
            app.logger.error("[BACK][models/health_professional.py][email.setter] L'email n'est pas du type string")
            raise TypeError("L'email n'est pas du type string")

        cleaned_email = value.strip()
        if not is_valid(cleaned_email, EMAIL_PATTERN):
            app.logger.error("[BACK][models/health_professional.py][email.setter] Le champ de l'email ne respecte pas le bon format")
            raise ValueError("Le champ de l'email ne respect pas le bon format")

        app.logger.info(f"[BACK][models/health_professional.py][email.setter] L'email {cleaned_email} est validé")
        self._email = cleaned_email

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if value is None:
            self._address = None
            return

        if not isinstance(value, str):
            app.logger.error("[BACK][models/health_professional.py][address.setter] L'adresse du professionnel doit être une chaîne de caractères")
            raise TypeError("L'adresse du professionnel doit être une chaîne de caractères")

        cleaned_address = value.strip()
        if len(cleaned_address) < 2 or len(cleaned_address) > 100:
            app.logger.error("[BACK][models/health_professional.py][address.setter] L'adresse doit comporter entre 2 et 100 caractères")
            raise ValueError("L'adresse du professionnel doit comporter entre 2 et 100 caractères")

        app.logger.info("[BACK][models/health_professional.py][address.setter] L'adresse du professionnel est validé")
        self._address = cleaned_address.title()


    @property
    def postal_code(self):
        return self._postal_code

    @postal_code.setter
    def postal_code(self, value):
        if value is None:
            self._postal_code = None
            return

        if not isinstance(value, str):
            app.logger.error("[BACK][models/health_professional.py][postal_code.setter] Le code postal du professionnel doit être une chaîne de caractères")
            raise TypeError("Le code postal du professionnel doit être une chaîne de caractères")

        cleaned__postal_code = value.strip()
        if len(cleaned__postal_code) < 5 or len(cleaned__postal_code) > 10:
            app.logger.error("[BACK][models/health_professional.py][postal_code.setter] Le code postal doit comporter entre 5 et 10 caractères")
            raise ValueError("Le code postal du professionnel doit comporter entre 5 et 10 caractères")

        app.logger.info("[BACK][models/health_professional.py][postal_code.setter] Le code postal du professionnel est validé")
        self._postal_code = cleaned__postal_code


    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if value is None:
            self._city = None
            return

        if not isinstance(value, str):
            app.logger.error("[BACK][models/health_professional.py][city.setter] City n'est pas du type string")
            raise TypeError("City n'est pas du type string")

        cleaned_city = value.strip()
        if not is_valid(cleaned_city, CITY_PATTERN):
            app.logger.error("[BACK][models/health_professional.py][city.setter] Le champ city ne respecte pas le bon format")
            raise ValueError("Le champ city ne respect pas le bon format")

        app.logger.info("[BACK][models/health_professional.py][city.setter] La city est validé")
        self._city = cleaned_city


    def to_dict(self):
        data = super().to_dict()
        documents_list = []
        documents = self.documents or []

        for document in documents:                              # type: ignore
            documents_list.append(document.to_dict())

        data["documents"] = documents_list
        notes_list = []
        notes = self.notes or []

        for note in notes:                                      # type: ignore
            notes_list.append(note.to_dict())

        data["notes"] = notes_list
        return data
