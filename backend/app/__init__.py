import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.utils.logging import configure_logging
from datetime import timedelta

# Global extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()


def create_app(test_config=None):
    """Create and configure the Flask application"""

    # Load environment variables
    load_dotenv()

    # Create Flask app instance
    flask_app = Flask(__name__, instance_relative_config=True)

    # Apply configuration
    if isinstance(test_config, dict):
        flask_app.config.from_mapping(test_config)
    else:
        env = os.environ.get("FLASK_ENV", "development")
        if test_config == "testing" or env == "testing":
            flask_app.config.from_object("config.TestingConfig")
        elif env == "production":
            flask_app.config.from_object("config.ProductionConfig")
        else:
            flask_app.config.from_object("config.DevelopmentConfig")

    # JWT and cookie configuration
    flask_app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    flask_app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    flask_app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"

    flask_app.config["JWT_COOKIE_SECURE"] = False
    flask_app.config["JWT_COOKIE_HTTPONLY"] = True
    flask_app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    flask_app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    # En production HTTPS: samesite="None" + secure=True

    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=48)

    # Mail configuration
    flask_app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    flask_app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    flask_app.config["MAIL_USE_TLS"] = True
    flask_app.config["MAIL_USE_SSL"] = False
    flask_app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    flask_app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    flask_app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "noreply@sweet-app.fr")

    # Initialize Flask extensions
    db.init_app(flask_app)
    mail.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)
    jwt.init_app(flask_app)
    configure_logging(flask_app)

    # Frontend configuration
    CORS(
        flask_app,
        supports_credentials=True,
        origins=["http://localhost:5173", "https://sweetapp.fr", "https://www.sweetapp.fr"]
    )

    # Register models
    import app.models

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.activity_routes import activity_bp
    from .routes.article_routes import article_bp
    from .routes.forum_routes import forum_bp
    from .routes.glycemia_routes import glycemia_bp
    from .routes.meal_routes import meal_bp
    from .routes.medication_routes import medication_bp
    from .routes.mood_routes import mood_bp
    from .routes.note_routes import note_bp
    from .routes.health_document_routes import document_bp
    from .routes.professional_routes import professional_bp
    from .routes.weight_routes import weight_bp
    from .routes.comment_routes import comment_bp

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(activity_bp)
    flask_app.register_blueprint(article_bp)
    flask_app.register_blueprint(forum_bp)
    flask_app.register_blueprint(glycemia_bp)
    flask_app.register_blueprint(meal_bp)
    flask_app.register_blueprint(medication_bp)
    flask_app.register_blueprint(mood_bp)
    flask_app.register_blueprint(note_bp)
    flask_app.register_blueprint(document_bp)
    flask_app.register_blueprint(professional_bp)
    flask_app.register_blueprint(weight_bp)
    flask_app.register_blueprint(comment_bp)

    # Ensure instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    # Health check route
    @flask_app.route("/ping")
    def ping():
        """Return a simple backend health check"""
        return {"status": "ok", "message": "Sweet backend is running", "env": env}

    return flask_app
