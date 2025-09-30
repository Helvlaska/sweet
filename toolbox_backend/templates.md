# Templates

### Template de classe :

```python
from models.base import BaseClass
from models import db

class ClassName(BaseClass):
    """
    TODO: Décrire la classe en une phrase
    Hérite de BaseClass (id, created_at, updated_at, CRUD).
    """

    __tablename__ = "table_name"  # TODO: nom SQL clair et cohérent

    # === Champs spécifiques ===
    field1 = db.Column(db.String(120), nullable=False)   # TODO: remplacer
    field2 = db.Column(db.Integer, nullable=True)        # TODO: remplacer

    # === Relations ===
    # TODO: exemple relation 1-n
    # children = db.relationship("OtherClass", backref="parent", cascade="all, delete")

    # === Méthodes métiers ===
    # TODO: ajouter si besoin (ex: calculs, validations spécifiques)

    def __repr__(self):
        return f"<ClassName {self.id}>"
```
