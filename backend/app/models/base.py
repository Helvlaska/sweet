from datetime import datetime
import uuid

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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
        for key, value in self.__dict__.items():
            if key in exclude:
                continue
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

# ---------------------------------------------------------------------- save()
    def save(self):
        """Met à jour le timestamp de modification"""
        self.updated_at = datetime.now()

# -------------------------------------------------------------------- update()
    def update(self, data):
        """Met à jour les attributs de l’instance à partir d’un dictionnaire"""
        for key, value in data.items():
            valid_attrs = self.__dict__.keys()
            if not hasattr(self, key):
                raise AttributeError(
                    f"{key} is not valid attribute"
                    f"Valid attributes are: {list(valid_attrs)}"
                )
            setattr(self, key, value)
        self.save()
