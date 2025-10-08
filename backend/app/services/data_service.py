from flask import current_app as app
from app import db
from app.models.glycemia import Glycemia
from app.models.weight import Weight

def validate_glycemia_data(data: dict) -> Glycemia:
    """Vérification du contenu de la requete"""
    try:
        glycemia = Glycemia(**data)
        app.logger.info("[BACK][services/data_service.py][validate_glycemia_data] La valeur glycémique est valide")
        return glycemia
    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_glycemia_data] Erreur de validation de la glycémie: {str(e)}")
        raise

def create_glycemia_entry(user_id, data):
    """Crée une nouvelle entrée pour un user via son id"""
    try:
        glycemia = validate_glycemia_data(data)
        glycemia.user_id = user_id
        glycemia.save()
        app.logger.info(f"[BACK][services/data_service.py][create_glycemia_entry()] Mesure {glycemia.glucose_level} mg/dL enregistrée pour le user {user_id}")
        return glycemia
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_glycemia_entry()] Erreur lors de la création: {e}")
        raise

def get_glycemia_entries(user_id, range_type):
    """Récupération des glycémies pour un jour donné"""
    pass

def update_glycemia_entrie(user_id):
    pass

def get_glycemia_stats(user_id, range_type):
    pass

def delete_glycemia_entries(entry_id, user_id):
    pass


