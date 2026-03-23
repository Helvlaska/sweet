"""
[BACK][models/health_document.py]

HealthDocument model — inherits from BaseModel (id, created_at, updated_at, entry_date, CRUD).

Fields:
  filename               String (255), validated extension (.pdf, .jpg, .jpeg, .png)
  file                   LargeBinary, base64 or bytes, max 5 MB
  health_professional_id Foreign key → health_professionals.id (nullable, SET NULL on delete)
  user_id                Foreign key → users.id

All fields are exposed via validated property setters.
file getter returns base64-encoded string for frontend consumption.
Max 10 documents per health professional (enforced in service layer).
"""


from flask import current_app as app
from app import db
from app.models.base import BaseModel
import base64


class HealthDocument(BaseModel) :
    __tablename__="health_documents"

    _filename = db.Column(db.String(255), nullable=False)
    _file = db.Column(db.LargeBinary, nullable=False)

    health_professional_id = db.Column(db.String(36), db.ForeignKey("health_professionals.id", ondelete="SET NULL"), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    ALLOWED_EXTENSIONS = (".pdf", ".jpg", ".jpeg", ".png")
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][health_document][filename] Type invalide")
            raise TypeError("Le nom du fichier doit être une chaîne")

        cleaned_filename = value.strip()

        if not (3 <= len(cleaned_filename) <= 255):
            app.logger.error("[BACK][health_document][filename] Longueur invalide")
            raise ValueError("Le nom du fichier doit comporter entre 3 et 255 caractères")

        lower_name = cleaned_filename.lower()

        if not lower_name.endswith(self.ALLOWED_EXTENSIONS):
            app.logger.error("[BACK][health_document][filename] Extension non autorisée")
            raise ValueError("Type de fichier non autorisé (.pdf, .jpg, .jpeg, .png)")

        app.logger.info("[BACK][health_document][filename] Nom validé")
        self._filename = cleaned_filename


    @property
    def file(self):
        try:
            encoded_file = base64.b64encode(self._file).decode("utf-8")
            return encoded_file
        except Exception as e:
            app.logger.error(f"[BACK][health_document][file.getter] Erreur encodage : {str(e)}")
            return None

    @file.setter
    def file(self, value):
        if value is None:
            app.logger.error("[BACK][health_document][file] Fichier manquant")
            raise ValueError("Le fichier est obligatoire")

        if isinstance(value, str):
            try:
                if "," in value:
                    value = value.split(",")[1]

                decoded_file = base64.b64decode(value)

            except Exception as e:
                app.logger.error(f"[BACK][health_document][file] Base64 invalide : {str(e)}")
                raise ValueError("Format base64 invalide")

        elif isinstance(value, (bytes, bytearray)):
            decoded_file = value

        else:
            app.logger.error("[BACK][health_document][file] Type non supporté")
            raise TypeError("Le fichier doit être en base64 ou en bytes")

        file_size = len(decoded_file)

        if file_size > self.MAX_FILE_SIZE:
            app.logger.error("[BACK][health_document][file] Fichier trop volumineux")
            raise ValueError("Le fichier dépasse la taille maximale autorisée (5 MB)")

        app.logger.info("[BACK][health_document][file] Fichier validé et enregistré")
        self._file = decoded_file
