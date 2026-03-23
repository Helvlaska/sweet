"""
[BACK][models/user.py]

User model — inherits from BaseModel (id, created_at, updated_at, entry_date, CRUD).

Fields:
  email, username, password_hash (write-only),
  first_name, last_name, date_of_birth, gender,
  height, city, profile_picture, role, first_login

All sensitive fields are exposed via validated property setters.
Password is hashed via bcrypt — never stored in plain text.

Relationships:
  Health data    (cascade delete) : activity, glycemia, meal, medication, mood, weight
  Medical record (cascade delete) : health_professional, note, health_documents
  Community      (no cascade)     : comment, forum_post, liked_posts,
                                    liked_comments, liked_articles
"""

from flask import current_app as app
from datetime import date, datetime
from app import db, bcrypt
from app.models.base import BaseModel
from app.utils.validators import is_valid, EMAIL_PATTERN, USERNAME_PATTERN, PASSWORD_PATTERN, FIRSTNAME_PATTERN, LASTNAME_PATTERN, CITY_PATTERN
import base64


class User(BaseModel):
    __tablename__ = "users"

    _email = db.Column(db.String(254), nullable=False, unique=True)
    _username = db.Column(db.String(30), nullable=False, unique=True)
    _password_hash = db.Column(db.String(255), nullable=False)
    _first_name = db.Column(db.String(75), nullable=False)
    _last_name = db.Column(db.String(100), nullable=False)
    _date_of_birth = db.Column(db.Date, nullable=True)
    _gender = db.Column(db.Enum("male", "female", "other", "prefer_not_say"), nullable=False, default="prefer_not_say")
    _height = db.Column(db.Integer, nullable=False)
    _city = db.Column(db.String(120), nullable=False)
    _profile_picture = db.Column(db.LargeBinary, nullable=True)
    _role = db.Column(db.Enum("user", "admin"), nullable=False, default="user")
    _first_login = db.Column(db.Boolean, nullable=False, default=True)

    comment = db.relationship("Comment", backref="user", cascade="all")
    forum_post = db.relationship("ForumPost", backref="user", cascade="all")
    activity = db.relationship("Activity", backref="user", cascade="all, delete-orphan")
    glycemia = db.relationship("Glycemia", backref="user", cascade="all, delete-orphan")
    meal = db.relationship("Meal", backref="user", cascade="all, delete-orphan")
    medication = db.relationship("Medication", backref="user", cascade="all, delete-orphan")
    mood = db.relationship("Mood", backref="user", cascade="all, delete-orphan")
    weight = db.relationship("Weight", backref="user", cascade="all, delete-orphan")
    health_professional = db.relationship("HealthProfessional", backref="user", cascade="all, delete-orphan")
    note = db.relationship("Note", backref="user", cascade="all, delete-orphan")
    health_documents = db.relationship("HealthDocument", backref="user", cascade="all, delete-orphan")
    liked_posts = db.relationship("ForumPost", secondary="user_likes_post", backref="liked_by", lazy="dynamic")
    liked_comments = db.relationship("Comment", secondary="user_likes_comment", backref="liked_by", lazy="dynamic")
    liked_articles = db.relationship("Article", secondary="user_likes_article", backref="liked_by", lazy="dynamic")


    @property
    def email(self):
        """L'email du user est privé"""
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/user.py][email.setter] L'email n'est pas du type string")
            raise TypeError("L'email n'est pas du type string")

        cleaned_email = value.strip()

        if not cleaned_email:
            app.logger.error("[BACK][models/user.py][email.setter] Le champ de l'email est vide")
            raise ValueError("Le champ de l'email est vide")

        if not is_valid(cleaned_email, EMAIL_PATTERN):
            app.logger.error(
                "[BACK][models/user.py][email.setter] Le champ de l'email ne respecte pas le bon format"
            )
            raise ValueError("Le champ de l'email ne respect pas le bon format")

        app.logger.info(f"[BACK][models/user.py][email.setter] L'email {cleaned_email} est validé")
        self._email = cleaned_email


    @property
    def username(self):
        """User's username"""
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/user.py][username.setter] Username n'est pas du type string")
            raise TypeError("Le username n'est pas du type string")

        cleaned_username = value.strip()

        if not cleaned_username:
            app.logger.error("[BACK][models/user.py][username.setter] Le champ du username est vide")
            raise ValueError("Le champ du username est vide")

        if not is_valid(cleaned_username, USERNAME_PATTERN):
            app.logger.error(
                "[BACK][models/user.py][username.setter] Le champ du username ne respecte pas le bon format"
            )
            raise ValueError("Le champ du username ne respect pas le bon format")

        app.logger.info(
            f"[BACK][models/user.py][username.setter] Le username {cleaned_username} est validé"
        )
        self._username = cleaned_username


    @property
    def password_hash(self):
        """Le mot de passe n'est pas accessible en lecture"""
        app.logger.error(
            "[BACK][models/user.py][password_hash.property] Le password n'est pas accessible en lecture"
        )
        raise AttributeError("Le password n'est pas accessible en lecture")

    @password_hash.setter
    def password_hash(self, value):
        if not isinstance(value, str):
            app.logger.error(
                "[BACK][models/user.py][password_hash.setter] Le champ du password doit être une string"
            )
            raise TypeError("Le password doit être une chaîne")

        cleaned_password_hash = value.strip()

        if not cleaned_password_hash:
            app.logger.error(
                "[BACK][models/user.py][password_hash.setter] Le champ du password ne peu pas être vide"
            )
            raise ValueError("Le password ne peut pas être vide")

        if not is_valid(cleaned_password_hash, PASSWORD_PATTERN):
            app.logger.error(
                "[BACK][models/user.py][password_hash.setter] Le champ du password ne respecte pas le bon format"
            )
            raise ValueError("Le champ du password ne respect pas le bon format")

        app.logger.info("[BACK][models/user.py][password_hash.setter] Le password est validé")
        self._password_hash = (bcrypt.generate_password_hash(cleaned_password_hash).decode('utf-8'))

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self._password_hash, password)


    @property
    def first_name(self):
        """User's first_name"""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/user.py][first_name.setter] First_name n'est pas du type string")
            raise TypeError("Le first_name n'est pas du type string")

        cleaned_first_name = value.strip()

        if not cleaned_first_name:
            app.logger.error("[BACK][models/user.py][first_name.setter] Le champ du first_name est vide")
            raise ValueError("Le champ du first_name est vide")

        if not is_valid(cleaned_first_name, FIRSTNAME_PATTERN):
            app.logger.error(
                "[BACK][models/user.py][first_name.setter] Le champ du first_name ne respecte pas le bon format"
            )
            raise ValueError("Le champ du first_name ne respect pas le bon format")

        app.logger.info("[BACK][models/user.py][first_name.setter] Le first_name est validé")
        self._first_name = cleaned_first_name


    @property
    def last_name(self):
        """User's last_name"""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/user.py][last_name.setter] Last_name n'est pas du type string")
            raise TypeError("Le last_name n'est pas du type string")

        cleaned_last_name = value.strip()

        if not cleaned_last_name:
            app.logger.error("[BACK][models/user.py][last_name.setter] Le champ du last_name est vide")
            raise ValueError("Le champ du last_name est vide")

        if not is_valid(cleaned_last_name, LASTNAME_PATTERN):
            app.logger.error(
                "[BACK][models/user.py][last_name.setter] Le champ du last_name ne respecte pas le bon format"
            )
            raise ValueError("Le champ du last_name ne respect pas le bon format")

        app.logger.info("[BACK][models/user.py][last_name.setter] Le last_name est validé")
        self._last_name = cleaned_last_name


    @property
    def date_of_birth(self):
        """User's date_of_birth"""
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        if value is None or value == "":
            app.logger.info(
                "[BACK][models/user.py][date_of_birth.setter] Aucun champ de date renseigné (nullable autorisé)."
            )
            self._date_of_birth = None
            return

        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
                app.logger.info(
                    "[BACK][models/user.py][date_of_birth.setter] Date_of_birth convertie depuis une chaîne ISO."
                )
            except ValueError:
                app.logger.error(
                    "[BACK][models/user.py][date_of_birth.setter] Format invalide. Attendu : YYYY-MM-DD."
                )
                raise ValueError("Format de la date invalide. Utilisez le format YYYY-MM-DD.")

        if not isinstance(value, date):
            app.logger.error(
                "[BACK][models/user.py][date_of_birth.setter] Date_of_birth n'est pas une date jj/mm/aaaa"
            )
            raise TypeError("La date de naissance doit être un objet date")

        if value.year <= 1900 or value >= date.today():
            app.logger.error(
                "[BACK][models/user.py][date_of_birth.setter] Date_of_birth est postérieur à la date du jour ou antérieur à 1900"
            )
            raise ValueError("La date de naissance ne peut pas être dans le futur ou trop loin dans le passé")

        app.logger.info("[BACK][models/user.py][date_of_birth.setter] Date_of_birth est validé")
        self._date_of_birth = value


    @property
    def gender(self):
        """Le genre de l'utilisateur"""
        return self._gender

    @gender.setter
    def gender(self, value):
        allowed = {"male", "female", "other", "prefer_not_say"}

        if not isinstance(value, str):
            app.logger.error("[BACK][models/user.py][gender.setter] Le gender doit être une string")
            raise TypeError("Le genre doit être une chaîne")

        if value not in allowed:
            app.logger.error(
                f"[BACK][models/user.py][gender.setter] Le champ gender doit être parmi {allowed}"
            )
            raise ValueError(f"Le genre doit être parmi {allowed}")

        app.logger.info("[BACK][models/user.py][gender.setter] Le champ gender est validé")
        self._gender = value


    @property
    def height(self):
        """User's height"""
        return self._height

    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            app.logger.error("[BACK][models/user.py][height.setter] La taille doit être un integer")
            raise TypeError("La taille doit être un entier (cm)")

        if value < 30 or value > 300:
            app.logger.error(
                "[BACK][models/user.py][height.setter] La taille doit être comprise entre 30 et 300 cm"
            )
            raise ValueError("La taille doit être comprise entre 30 et 300 cm")

        app.logger.info("[BACK][models/user.py][height.setter] Le champ height est validé")
        self._height = value


    @property
    def city(self):
        """User's city"""
        return self._city

    @city.setter
    def city(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/user.py][city.setter] City n'est pas du type string")
            raise TypeError("City n'est pas du type string")

        cleaned_city = value.strip()

        if not cleaned_city:
            app.logger.error("[BACK][models/user.py][city.setter] Le champ city est vide")
            raise ValueError("Le champ city est vide")

        if not is_valid(cleaned_city, CITY_PATTERN):
            app.logger.error(
                "[BACK][models/user.py][city.setter] Le champ city ne respecte pas le bon format"
            )
            raise ValueError("Le champ city ne respect pas le bon format")

        app.logger.info("[BACK][models/user.py][city.setter] La city est validé")
        self._city = cleaned_city


    @property
    def profile_picture(self):
        """User's profile_picture"""
        if not self._profile_picture:
            return None

        try:
            encoded_image = base64.b64encode(self._profile_picture).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded_image}"
        except Exception as e:
            app.logger.error(
                f"[BACK][models/user.py][profile_picture.getter] Erreur encodage base64 : {str(e)}"
            )
            return None

    @profile_picture.setter
    def profile_picture(self, value):
        if value is None:
            self._profile_picture = None
            app.logger.info(
                "[BACK][models/user.py][profile_picture.setter] Aucune profile_picture n'a été ajoutée"
            )
            return

        if isinstance(value, str):
            try:
                if value.startswith("data:image"):
                    value = value.split(",")[1]
                decoded_image = base64.b64decode(value)
                self._profile_picture = decoded_image
                app.logger.info(
                    "[BACK][models/user.py][profile_picture.setter] Image base64 décodée avec succès"
                )
            except Exception as e:
                app.logger.error(
                    f"[BACK][models/user.py][profile_picture.setter] Erreur décodage base64 : {str(e)}"
                )
                raise ValueError("Format base64 invalide pour la photo de profil")
            return

        if not isinstance(value, (bytes, bytearray)):
            app.logger.error(
                "[BACK][models/user.py][profile_picture.setter] Le champ profile_picture doit être une image (bytes ou base64)"
            )
            raise TypeError("La photo de profil doit être une image (bytes ou base64)")

        app.logger.info(
            "[BACK][models/user.py][profile_picture.setter] La profile_picture est validée (format bytes)"
        )
        self._profile_picture = value


    @property
    def first_login(self):
        """User's first_login"""
        return self._first_login

    @first_login.setter
    def first_login(self, value):
        if not isinstance(value, bool):
            app.logger.error(
                "[BACK][models/user.py][first_login.setter] Le champ first_login doit être un boolean"
            )
            raise TypeError("first_login doit être un booléen (True/False)")

        app.logger.info(
            "[BACK][models/user.py][first_login.setter] Le champ first_login est validé"
        )
        self._first_login = value


    @property
    def role(self):
        """User's role"""
        return self._role

    @role.setter
    def role(self, value):
        allowed = {"user", "admin"}

        if not isinstance(value, str):
            app.logger.error(
                "[BACK][models/user.py][role.setter] Le champ role doit être une string"
            )
            raise TypeError("Le rôle doit être une chaîne")

        if value not in allowed:
            app.logger.error(
                f"[BACK][models/user.py][role.setter] Le champ role doit être parmi {allowed}"
            )
            raise ValueError(f"Le rôle doit être parmi {allowed}")

        app.logger.info(
            "[BACK][models/user.py][role.setter] Le champ role est validé"
        )
        self._role = value
