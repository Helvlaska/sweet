from flask import current_app as app
from app.models import Activity
from app.utils import timelaps

def validate_activity_data(data: dict):
    """Validate and return a valid Activity instance"""
    try:
        activity = Activity()
        activity.description = data.get("description")
        activity.duration = data.get("duration")
        app.logger.info(f"[BACK][services/activity_service.py][validate_activity_data] L'activité {activity.description} de {activity.duration} minutes sont valides")
        return activity

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/activity_service.py][validate_activity_data] Erreur de validation de l'activité: {str(e)}")
        raise


def create_activity_entry(user_id: str, data: dict):
    """Create and save a new Activity entry"""
    try:
        activity = validate_activity_data(data)
        activity.user_id = user_id
        activity.save()
        app.logger.info(f"[BACK][services/activity_service][create_activity_entry] L'activité {activity.description} pendant {activity.duration} minutes à été enregistrée pour le user {user_id}")
        return activity.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/activity_service][create_activity_entry] Erreur lors de la création de l'activité '{activity.description}' pour le user {user_id}: {e}")
        raise


def get_activity_entry(user_id: str, range_type: str, target_date=None):
    """Retrieve activity entries filtered by date range"""
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Activity.query.filter(Activity.user_id == user_id, Activity.entry_date >= start_date, Activity.entry_date <= end_date).order_by(Activity.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/activity_service][get_activity_entry] Aucune entrée trouvée pour l’utilisateur {user_id} ({range_type}).")
            return []
        app.logger.info(f"[BACK][services/activity_service][get_activity_entry] {len(entries)} entrées trouvées pour l'utilisateur {user_id}, {range_type} → {start_date} à {end_date}") # type: ignore
        result = []
        for entry in entries:
            activity_dict = entry.to_dict()
            result.append(activity_dict)
        return result

    except ValueError as e:
        app.logger.error(f"[BACK][services/activity_service][get_activity_entry] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/activity_service][get_activity_entry] Erreur inattendue : {e}")
        raise


def update_activity_entry(user_id: str, entry_id: str, new_data: dict):
    """Update an Activity entry fields"""
    try:
        entry = Activity.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/activity_service][update_activity_entry] Aucune entrée trouvée pour cet utilisateur")
            return None
        app.logger.info(f"[BACK][services/activity_service][update_activity_entry] L'activités {entry.description} de {entry.duration} minutes: trouvé")
        if "description" in new_data:
            validated_description = validate_activity_data({"description": new_data["description"], "duration": entry.duration})
            entry.description = validated_description.description
        if "duration" in new_data:
            validated_duration = validate_activity_data({"duration": new_data["duration"], "description": entry.description})
            entry.duration = validated_duration.duration
        entry.save()
        app.logger.info(f"[BACK][services/activity_service][update_activity_entry] Entrée {entry_id} mise à jour de l'activité {entry.description} pendant {entry.duration} minutes, pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/activity_service][update_activity_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/activity_service][update_activity_entry] Erreur inattendue : {e}")
        raise


def get_activity_stats(user_id: str, range_type: str, target_date=None):
    """Compute average activity duration for a user"""
    try:
        entries = get_activity_entry(user_id, range_type, target_date)
        if not entries:
            app.logger.info(f"[BACK][services/activity_service][get_activity_stats] Aucune donnée trouvée pour l’utilisateur {user_id} ({range_type})")
            return None
        app.logger.info(f"[BACK][services/activity_service][get_activity_stats] {len(entries)} enregistrements récupérés pour l’utilisateur {user_id} ({range_type})")
        values = []
        for entry in entries:
            activity_value = entry["duration"]
            values.append(activity_value)
        if values:
            average = round((sum(values) / len(values)))
            app.logger.info(f"[BACK][services/activity_service][get_activity_stats] Moyenne calculée : {average} min/j sur {len(values)} enregistrements")
            return {"average": average}
        else:
            app.logger.info(f"[BACK][services/activity_service][get_activity_stats] Liste des valeurs vide malgré {len(entries)} enregistrements")
            return {"average": None}

    except ValueError as e:
        app.logger.error(f"[BACK][services/activity_service][get_activity_stats] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/activity_service][get_activity_stats] Erreur inattendue : {e}")
        raise


def delete_activity_entry(entry_id: str, user_id: str):
    """Delete a user Activity entry by ID"""
    try:
        entry = Activity.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/activity_service][delete_activity_entry] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/activity_service][delete_activity_entry] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/activity_service][delete_activity_entry] Erreur inattendue pour user {user_id}, entry {entry_id} : {e}")
        raise
