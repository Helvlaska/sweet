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


    # Save
    def save(self):
        """Add and commit the instance to the database"""
        try:
            db.session.add(self)
            db.session.commit()
            app.logger.info(f"[BACK][models/base.py][save] L'instance a bien été enregistrée en BDD: {self.__class__.__name__} (id={self.id})")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"[BACK][models/base.py][save()] Erreur lors de la sauvegarde de l'instance {self.__class__.__name__}: {e}")
            raise


    # Update
    def update(self, data):
        """Update instance attributes from a dictionary"""
        try:
            valid_attrs = {col.name for col in self.__table__.columns}  # type: ignore
            for key, value in data.items():
                if key not in valid_attrs:
                    app.logger.error(f"[BACK][models/base.py][update()] '{key}' is not a valid attribute for {self.__class__.__name__}")
                    raise AttributeError(f"'{key}' is not a valid attribute. Valid attributes: {list(valid_attrs)}")
                setattr(self, key, value)
            self.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            app.logger.info(f"[BACK][models/base.py][update()] {self.__class__.__name__} (id={self.id}) updated successfully")

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"[BACK][models/base.py][update()] Error while updating {self.__class__.__name__}: {e}")
            raise


    # Delete
    def delete(self):
        """Delete the instance from the database"""
        try:
            db.session.delete(self)
            db.session.commit()
            app.logger.info(f"[BACK][models/base.py][delete()] Entrée supprimée : {self.__class__.__name__} (id={self.id})")

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"[BACK][models/base.py][delete()] Erreur lors de la suppression : {e}")
            raise


    # Likes methode
    def increment_likes(self):
        """Increment the like counter for entities with a '_likes' field"""
        if not hasattr(self, "_likes"):
            app.logger.error(f"[BACK][models/base.py][increment_likes()] L'objet {self.__class__.__name__} n'est pas 'likable'")
            raise AttributeError(f"{self.__class__.__name__} ne possède pas d'attribut '_likes'")
        self._likes += 1
        app.logger.info(f"[BACK][models/base.py][increment_likes()] {self.__class__.__name__} {self.id} liké → total : {self._likes}")
        return self._likes


    # to_dict()
    def to_dict(self, exclude=None):
        """Return a dictionary representation of the instance"""
        if exclude is None:
            exclude = []
        result = {}
        for column in self.__table__.columns:            # type: ignore
            if column.name in exclude:
                continue
            if str(column.type).lower() in ("largebinary", "blob", "bytea"):
                continue
            key = column.name.lstrip("_")
            value = getattr(self, column.name)
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            result[key] = value
        return result
