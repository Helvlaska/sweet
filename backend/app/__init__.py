import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.utils.logging import configure_logging
from datetime import timedelta

# ----------------------------------------------- Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()

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

# --------------------------- Configuration des tokens et des cookies sécurisés
    # Déclaration d'utilisation des cookies
    flask_app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    # Déclaration du path pour chaque token
    flask_app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    flask_app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"

    # Configuration de la sécurité des cookies
    flask_app.config["JWT_COOKIE_SECURE"] = False  # ⚠️ Mettre True en production (HTTPS obligatoire)
    flask_app.config["JWT_COOKIE_HTTPONLY"] = True
    flask_app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    flask_app.config["JWT_COOKIE_SAMESITE"] = "Lax"

    # Configuration de la durée de vie des tokens
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=48)

# ------------------------------------------------- Configuration de Flask-Mail
    flask_app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    flask_app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    flask_app.config["MAIL_USE_TLS"] = True
    flask_app.config["MAIL_USE_SSL"] = False
    flask_app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    flask_app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    flask_app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "noreply@sweet-app.fr")

# --------------------------------------------------- Initialisation extensions
    db.init_app(flask_app)
    mail.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)
    jwt.init_app(flask_app)
    configure_logging(flask_app)

# -------------------------------------------------- Enregistrement des modèles
    import app.models

# ----------------------------------------------- Enregistrement des blueprints
    # Exemple :
    # from .routes.auth import auth_bp
    # flask_app.register_blueprint(auth_bp)
    from .routes.auth import auth_bp
    from .routes.data import data_bp
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(data_bp)

# ------------------------------------------------------------- Instance folder
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

# ------------------------------------------------------------------ Route test
    @flask_app.route("/ping")
    def ping():
        return {"status": "ok", "message": "Sweet backend is running", "env": flask_app.config["ENV"]}

    return flask_app
