import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# ----------------------------------------------- Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(test_config=None):
    """Fonction pour créer et configurer l'application Flask"""

# ---------------------------------------------------------------- Charger .env
    load_dotenv()

# --------------------------------------------- Création de l'application Flask
    flask_app = Flask(__name__, instance_relative_config=True)

# ------------------------------------------------------------ Sélection config
    if test_config is None:
        env = os.environ.get("FLASK_ENV", "development")
        if env == "production":
            flask_app.config.from_object("config.ProductionConfig")
        elif env == "testing":
            flask_app.config.from_object("config.TestingConfig")
        else:
            flask_app.config.from_object("config.DevelopmentConfig")
    else:
        # Config spéciale test si donnée
        flask_app.config.from_mapping(test_config)

# --------------------------------------------------- Initialisation extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)

# -------------------------------------------------- Enregistrement des modèles
    import app.models

# ----------------------------------------------- Enregistrement des blueprints
    # Exemple :
    # from .routes.auth import auth_bp
    # flask_app.register_blueprint(auth_bp)
    from .routes.auth import auth_bp
    flask_app.register_blueprint(auth_bp)

# ------------------------------------------------------------- Instance folder
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

# ------------------------------------------------------------------ Route test
    @flask_app.route("/ping")
    def ping():
        return {"status": "ok", "message": "Sweet backend is running"}

    return flask_app
