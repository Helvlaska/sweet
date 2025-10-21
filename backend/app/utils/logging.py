import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def configure_logging(app):
    """Configure un logger unique pour toute l'application."""

    # --- Dossier des logs ---
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../logs")
    os.makedirs(log_dir, exist_ok=True)

    # --- Choix du fichier selon le mode ---
    if app.config.get("TESTING"):
        log_file = os.path.join(log_dir, "tests_run.log")  # ✅ un seul fichier unique
    else:
        log_file = os.path.join(log_dir, "app.log")

    # --- Format du log ---
    log_format = "[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # --- Handler rotatif (évite fichiers géants > 5 Mo) ---
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # --- Log console ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --- Application au logger Flask ---
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    # --- Marque visuelle d'une nouvelle session ---
    separator = "\n" + "=" * 80 + "\n"
    session_header = (
        f"{separator}"
        f"🧪 Nouvelle session de tests SWEET — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{separator}"
    )
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(session_header)

    app.logger.info("✅ Logger SWEET configuré — les logs seront ajoutés à la suite dans logs/tests_run.log.")
