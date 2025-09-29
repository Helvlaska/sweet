import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    """Fonction pour créer et configurer l'application Flask"""

    # ------------------------------------------------------------ Charger .env
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # -------------------------------------------------------- Sélection config
    if test_config is None:
        env = os.environ.get("FLASK_ENV", "development")
        if env == "production":
            app.config.from_object("config.ProductionConfig")
        elif env == "testing":
            app.config.from_object("config.TestingConfig")
        else:
            app.config.from_object("config.DevelopmentConfig")
    else:
        # Config spéciale test si donnée
        app.config.from_mapping(test_config)

    # ----------------------------------------------- Initialisation extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ------------------------------------------- Enregistrement des blueprints
    # Exemple :
    # from .routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    # --------------------------------------------------------- Instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # -------------------------------------------------------------- Route test
    @app.route("/ping")
    def ping():
        return {"status": "ok", "message": "Sweet backend is running"}

    return app
