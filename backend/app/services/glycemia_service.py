from flask import current_app as app
from app.models import Glycemia
from app.utils import timelaps


def validate_glycemia_data(data: dict):
    try:
        if not data:
            app.logger.error("[BACK][services/data_service.py][validate_glycemia_data] Aucune donnée reçue.")
            raise ValueError("Aucune donnée reçue pour la création de la mesure de glycémie")
        glycemia = Glycemia()
        glycemia.glucose_level = data.get("glucose_level")
        app.logger.info("[BACK][services/data_service.py][validate_glycemia_data] La valeur glycémique est valide")
        return glycemia

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_glycemia_data] Erreur de validation de la glycémie: {str(e)}")
        raise


def create_glycemia_entry(user_id: str, data: dict):
    try:
        glycemia = validate_glycemia_data(data)
        glycemia.user_id = user_id
        glycemia.save()
        app.logger.info(f"[BACK][services/data_service.py][create_glycemia_entry()] Mesure {glycemia.glucose_level} mg/dL enregistrée pour le user {user_id}")
        return glycemia.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_glycemia_entry()] Erreur lors de la création: {e}")
        raise


def get_glycemia_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Glycemia.query.filter(Glycemia.user_id == user_id, Glycemia.entry_date >= start_date, Glycemia.entry_date <= end_date).order_by(Glycemia.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_glycemia_entries] Aucune entrée trouvée pour l’utilisateur {user_id} ({range_type}).")
            return []
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
    try:
        entry = Glycemia.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/data_services.py][update_glycemia_entries()] Aucune entrée trouvée pour cet utilisateur")
            return None
        app.logger.info(f"[BACK][services/data_service.py][update_glycemia_entry] Le mesure de {entry.glucose_level} trouvée pour le user {user_id}")
        validated_glucose_level = validate_glycemia_data({"glucose_level": new_data["glucose_level"]})
        entry.glucose_level = validated_glucose_level.glucose_level
        entry.save()
        app.logger.info(f"[BACK][services/data_services.py][update_glycemia_entries()] Entrée {entry_id} mise à jour à {validated_glucose_level} mg/dl pour user {user_id}")
        return entry.to_dict()

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
