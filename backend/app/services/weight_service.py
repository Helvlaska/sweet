from flask import current_app as app
from app.models import Weight
from app.utils import timelaps


def validate_weight_data(data: dict) -> Weight:
    try:
        weight = Weight()
        mass_value = data.get("mass") #type: ignore
        mass_value: float = float(data.get("mass", 0.0))
        weight.mass = mass_value
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
        app.logger.info(f"[BACK][services/data_service.py][create_weight_entries()] Mesure {weight.mass} kg enregistrée pour le user {user_id}")
        return weight.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_weight_entries()] Erreur lors de la création: {e}")
        raise


def get_weight_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Weight.query.filter(Weight.user_id == user_id, Weight.entry_date >= start_date, Weight.entry_date <= end_date).order_by(Weight.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_weight_entries] Aucune entrée trouvée pour l’utilisateur {user_id} ({range_type}).")
            return []
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
            app.logger.info("[BACK][services/data_service.py][update_weight_entry()] Aucune entrée trouvée pour cet utilisateur")
            return None
        app.logger.info(f"[BACK][services/data_service.py][update_weight_entry] L'entrée de {entry.mass} kg à été trouvée")
        validated_weight = validate_weight_data({"mass": new_data["mass"]})
        entry.mass = validated_weight.mass
        entry.save()
        app.logger.info(f"[BACK][services/data_service.py][update_weight_entry()] Entrée {entry_id} mise à jour à {entry.mass} kg pour user {user_id}")
        return entry.to_dict()

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
