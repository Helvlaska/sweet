from flask import current_app as app
from datetime import datetime, timezone
import uuid
from app import db

class BaseModel(db.Model):
    __abstract__= True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    entry_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(), index=True, nullable=False)

# ---------------------------------------------------------------------- save()
    def save(self):
        """Met à jour le timestamp de modification"""
        db.session.add(self)
        db.session.commit()

# -------------------------------------------------------------------- update()
    def update(self, data):
        """Met à jour les attributs de l’instance à partir d’un dictionnaire"""
        valid_attrs = {col.name for col in self.__table__.columns} # type: ignore
        for key, value in data.items():
            valid_attrs = self.__dict__.keys()
            if not hasattr(self, key):
                app.logger.error("[BACK][models/base.py][update()] '{key}' n'est pas un attribut valide")
                raise AttributeError(f"{key} is not valid attribute, Valid attributes are: {list(valid_attrs)}")
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

# ---------------------------------------------------------------------- delete()
    def delete(self):
        """Supprime l'instance de la base de données"""
        try:
            db.session.delete(self)
            db.session.commit()
            app.logger.info(f"[BACK][models/base.py][delete()] Entrée supprimée : {self.__class__.__name__} (id={self.id})")

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"[BACK][models/base.py][delete()] Erreur lors de la suppression : {e}")
            raise


# ------------------------------------------------------------ Méthode générique pour la gestion des likes
    def increment_likes(self):
        """
        Incrémente le compteur de likes pour les entités qui possèdent un champ _likes.
        """
        if not hasattr(self, "_likes"):
            app.logger.error(f"[BACK][models/base.py][increment_likes()] L'objet {self.__class__.__name__} n'est pas 'likable'")
            raise AttributeError(f"{self.__class__.__name__} ne possède pas d'attribut '_likes'")
        self._likes += 1
        app.logger.info(f"[BACK][models/base.py][increment_likes()] {self.__class__.__name__} {self.id} liké → total : {self._likes}")
        return self._likes


# ------------------------------------------------------------------- to_dict()
    def to_dict(self, exclude=None):
        """
        Retourne un dictionnaire représentant l’instance.
        exclude: liste des attributs à exclure (ex: mdp, token)
        exemple d'utilisation : print(user.to_dict(exclude=["password_hash"]))
        """
        if exclude is None:
            exclude = []
        result = {}
        for column in self.__table__.columns: # type: ignore
            if column.name not in exclude:
                result[column.name] = getattr(self, column.name)
        return result

