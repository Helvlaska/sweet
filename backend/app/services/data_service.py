from datetime import date
from flask import current_app as app
from sqlalchemy import delete
from app import db
from app.models.glycemia import Glycemia
from app.models.weight import Weight
from app.utils import timelaps

# -------------------------------------------------------------------- Glycemia
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

def get_glycemia_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    """Récupération les glycémies pour un jour/semaine/mois/3mois/6mois/1an donné"""
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Glycemia.query.filter(Glycemia.user_id, Glycemia.entry_date >= start_date, Glycemia.entry_date <= end_date).order_by(Glycemia.entry_date.asc()).all)
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_glycemia_entries] Aucune entrée trouvée pour l’utilisateur {user_id} ({range_type}).")
        app.logger.info(f"[BACK][services/data_services][create_glycemia_entries] {len(entries)} entrées trouvées pour l'utilisateur {user_id}, {range_type} → {start_date} à {end_date}") # type: ignore
        result = []
        for entry in entries: # type: ignore
            glycemia_dict = entry.to_dict()
            result.append(glycemia_dict)
        return result

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_glycemia_entries] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_glycemia_entries] Erreur inattendue : {e}")
        raise

def update_glycemia_entry(user_id: str, entry_id: str, new_data: dict):
    """Modifier une mesure déjà existante"""
    try:
        entry = Glycemia.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/data_services.py][update_glycemia_entries()] Aucune entrée trouvée pour cet utilisateur")
            return None
        validated = validate_glycemia_data(new_data)
        new_value = validated.glucose_level
        entry.glucose_level = new_value
        entry.save()
        app.logger.info(f"[BACK][services/data_services.py][update_glycemia_entries()] Entrée {entry_id} mise à jour à {new_value} mg/dl pour user {user_id}")
        return {"update_value": new_value}
    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_glycemia_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_glycemia_entry] Erreur inattendue : {e}")
        raise

def get_glycemia_stats(user_id: str, range_type: str, target_date=None):
    """calculer la moyenne des mesures"""
    try:
        entries = get_glycemia_entry(user_id, range_type, target_date)
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_glycemia_stats] Aucune donnée trouvée pour l’utilisateur {user_id} ({range_type})")
            return None
        app.logger.info(f"[BACK][services/data_service.py][get_glycemia_stats] {len(entries)} mesures récupérées pour l’utilisateur {user_id} ({range_type})")
        values = []
        for entry in entries:
            glycemia_value = entry["glucose_level"]
            values.append(glycemia_value)
        if values:
            average = round((sum(values) / len(values)))
            app.logger.info(f"[BACK][services/data_service.py][get_glycemia_stats] Moyenne calculée : {average} mg/dL sur {len(values)} mesures")
            return {"average": average}
        else:
            app.logger.info(f"[BACK][services/data_service.py][get_glycemia_stats] Liste des valeurs vide malgré {len(entries)} entrées")
            return {"average": None}

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_glycemia_stats] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_glycemia_stats] Erreur inattendue : {e}")
        raise

def delete_glycemia_entry(entry_id: str, user_id: str):
    """Supprimer une mesure de l'utilisateur"""
    try:
        entry = Glycemia.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_glycemia_entry] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_glycemia_entry] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_glycemia_entry] Erreur inattendue pour user {user_id}, entry {entry_id} : {e}")
        raise

# ---------------------------------------------------------------------- Weight
def validate_weight_data(data: dict) -> Weight:
    try:
        weight = Weight(**data)
        app.logger.info("[BACK][services/data_service.py][validate_weight_data] La valeur du poids est valide")
        return weight

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_weight_data] Erreur de validation du poids: {str(e)}")
        raise

def create_weight_entry(user_id, data):
    try:
        weight = validate_weight_data(data)
        weight.user_id = user_id
        weight.save()
        app.logger.info(f"[BACK][services/data_service.py][create_weight_entries()] Mesure {weight.mass} mg/dL enregistrée pour le user {user_id}")
        return weight

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_weight_entries()] Erreur lors de la création: {e}")
        raise

def get_weight_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Weight.query.filter(Weight.user_id, Weight.entry_date >= start_date, Weight.entry_date <= end_date).order_by(Weight.entry_date.asc()).all)
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_weight_entries] Aucune entrée trouvée pour l’utilisateur {user_id} ({range_type}).")
        app.logger.info(f"[BACK][services/data_services][get_weight_entries] {len(entries)} entrées trouvées pour l'utilisateur {user_id}, {range_type} → {start_date} à {end_date}") # type: ignore
        result = []
        for entry in entries: # type: ignore
            weight_dict = entry.to_dict()
            result.append(weight_dict)
        return result

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_weight_entries] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_weight_entries] Erreur inattendue : {e}")
        raise

def update_weight_entry(user_id: str, entry_id: str, new_data: dict):
    try:
        entry = Weight.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/data_services.py][update_weight_entry()] Aucune entrée trouvée pour cet utilisateur")
            return None
        validated = validate_weight_data(new_data)
        new_value = validated.mass
        entry.mass = new_value
        entry.save()
        app.logger.info(f"[BACK][services/data_services.py][update_weight_entry()] Entrée {entry_id} mise à jour à {new_value} mg/dl pour user {user_id}")
        return {"update_value": new_value}

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_weight_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_weight_entry] Erreur inattendue : {e}")
        raise

def get_weight_stats(user_id: str, range_type: str, target_date=None):
    try:
        entries = get_weight_entry(user_id, range_type, target_date)
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_weight_stats] Aucune donnée trouvée pour l’utilisateur {user_id} ({range_type})")
            return None
        app.logger.info(f"[BACK][services/data_service.py][get_weight_stats] {len(entries)} mesures récupérées pour l’utilisateur {user_id} ({range_type})")
        values = []
        for entry in entries:
            weight_value = entry["mass"]
            values.append(weight_value)
        if values:
            average = round((sum(values) / len(values)), 1)
            app.logger.info(f"[BACK][services/data_service.py][get_weight_stats] Moyenne calculée : {average} kg sur {len(values)} mesures")
            return {"average": average}
        else:
            app.logger.info(f"[BACK][services/data_service.py][get_weight_stats] Liste des valeurs vide malgré {len(entries)} entrées")
            return {"average": None}

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_weight_stats] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_weight_stats] Erreur inattendue : {e}")
        raise

def delete_weight_entry(entry_id: str, user_id: str):
    """Supprimer une mesure de l'utilisateur"""
    try:
        entry = Weight.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_weight_entries] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_weight_entries] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_weight_entries] Erreur inattendue pour user {user_id}, entry {entry_id} : {e}")
        raise
