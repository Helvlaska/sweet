import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    """Configure un logger unique pour toute l'application."""

    # --- Dossier et fichier de logs ---
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    # --- Format des messages ---
    log_format = "[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # --- Fichier de logs rotatif (évite les fichiers de 50 Mo) ---
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # --- Log console (pour les tests Postman ou Flask run) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --- Application du logger ---
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    app.logger.info("✅ Logger SWEET configuré avec succès — tous les logs dans logs/app.log.")
