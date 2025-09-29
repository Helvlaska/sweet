import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuration de base (utilisé par tout les environnements)"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev_jwt_key")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

class DevelopmentConfig(Config):
    """Configuration pour le développement local"""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "sweet_dev.db")
    )
    DEBUG = True

class TestingConfig(Config):
    """Configuration pour faire tourner les tests"""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "sweet_test.db")
    )
    TESTING = True

class ProductionConfig(Config):
    """Configuration pour la production"""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "mysql+pymysql://user:password@localhost/sweet"
    )
    DEBUG = False
    TESTING = False
