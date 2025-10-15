from flask import current_app as app
from app import db
from app.models import Glycemia, Weight, Activity, Meal, Mood, Medication, HealthProfessional, Note, ForumPost, Comment, Article, User
from app.utils import timelaps

# -------------------------------------------------------------------- Glycemia
def validate_glycemia_data(data: dict) -> Glycemia:
    try:
        glycemia = Glycemia()
        glycemia.glucose_level = data.get("glucose_level")
        app.logger.info("[BACK][services/data_service.py][validate_glycemia_data] La valeur glycémique est valide")
        return glycemia

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_glycemia_data] Erreur de validation de la glycémie: {str(e)}")
        raise


def create_glycemia_entry(user_id, data):
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


# ---------------------------------------------------------------------- Weight
def validate_weight_data(data: dict) -> Weight:
    try:
        weight = Weight()
        weight.mass = data.get("mass")
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


# ---------------------------------------------------------------------- Activity
def validate_activity_data(data: dict) -> Activity:
    try:
        activity = Activity()
        activity.description = data.get("description")
        activity.duration = data.get("duration")
        app.logger.info(f"[BACK][services/data_service.py][validate_activity_data] L'activité {activity.description} de {activity.duration} minutes sont valides")
        return activity

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_activity_data] Erreur de validation de l'activité: {str(e)}")
        raise


def create_activity_entry(user_id, data):
    try:
        activity = validate_activity_data(data)
        activity.user_id = user_id
        activity.save()
        app.logger.info(f"[BACK][services/data_service.py][create_activity_entry()] L'activité {activity.description} pendant {activity.duration} minutes à été enregistrée pour le user {user_id}")
        return activity.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_activity_entry()] Erreur lors de la création de l'activité '{activity.description}' pour le user {user_id}: {e}")
        raise


def get_activity_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Activity.query.filter(Activity.user_id == user_id, Activity.entry_date >= start_date, Activity.entry_date <= end_date).order_by(Activity.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_activity_entry] Aucune entrée trouvée pour l’utilisateur {user_id} ({range_type}).")
            return []
        app.logger.info(f"[BACK][services/data_services][get_activity_entry] {len(entries)} entrées trouvées pour l'utilisateur {user_id}, {range_type} → {start_date} à {end_date}") # type: ignore
        result = []
        for entry in entries: # type: ignore
            activity_dict = entry.to_dict()
            result.append(activity_dict)
        return result

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_activity_entry] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_activity_entry] Erreur inattendue : {e}")
        raise


def update_activity_entry(user_id: str, entry_id: str, new_data: dict):
    try:
        entry = Activity.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/data_service.py][update_activity_entry()] Aucune entrée trouvée pour cet utilisateur")
            return None
        app.logger.info(f"[BACK][services/data_service.py][update_activity_entry()] L'activités {entry.description} de {entry.duration} minutes: trouvé")
        if "description" in new_data:
            validated_description = validate_activity_data({"description": new_data["description"], "duration": entry.duration})
            entry.description = validated_description.description
        if "duration" in new_data:
            validated_duration = validate_activity_data({"duration": new_data["duration"], "description": entry.description})
            entry.duration = validated_duration.duration
        entry.save()
        app.logger.info(f"[BACK][services/data_service.py][update_activity_entry()] Entrée {entry_id} mise à jour de l'activité {entry.description} pendant {entry.duration} minutes, pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_activity_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_activity_entry] Erreur inattendue : {e}")
        raise


def get_activity_stats(user_id: str, range_type: str, target_date=None):
    try:
        entries = get_activity_entry(user_id, range_type, target_date)
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_activity_stats] Aucune donnée trouvée pour l’utilisateur {user_id} ({range_type})")
            return None
        app.logger.info(f"[BACK][services/data_service.py][get_activity_stats] {len(entries)} enregistrements récupérés pour l’utilisateur {user_id} ({range_type})")
        values = []
        for entry in entries:
            activity_value = entry["duration"]
            values.append(activity_value)
        if values:
            average = round((sum(values) / len(values)))
            app.logger.info(f"[BACK][services/data_service.py][get_activity_stats] Moyenne calculée : {average} min/j sur {len(values)} enregistrements")
            return {"average": average}
        else:
            app.logger.info(f"[BACK][services/data_service.py][get_activity_stats] Liste des valeurs vide malgré {len(entries)} enregistrements")
            return {"average": None}

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_activity_stats] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_activity_stats] Erreur inattendue : {e}")
        raise


def delete_activity_entry(entry_id: str, user_id: str):
    """Supprimer une mesure de l'utilisateur"""
    try:
        entry = Activity.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_activity_entry] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_activity_entry] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_activity_entry] Erreur inattendue pour user {user_id}, entry {entry_id} : {e}")
        raise


# ---------------------------------------------------------------------- Meal
def validate_meal_data(data: dict) -> Meal:
    try:
        meal = Meal()
        meal.description = data.get("description")
        meal.meal_type = data.get("meal_type")
        app.logger.info("[BACK][services/data_service.py][validate_meal_data] Les valeurs pour le repas sont valides")
        return meal

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_meal_data] Erreur de validation du repas: {str(e)}")
        raise


def create_meal_entry(user_id, data):
    try:
        meal = validate_meal_data(data)
        meal.user_id = user_id
        meal.save()
        app.logger.info(f"[BACK][services/data_service.py][create_meal_entry()] Le repas {meal.description} pour le {meal.meal_type} à été enregistrée pour le user {user_id}")
        return meal.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_meal_entry()] Erreur lors de la création du repas '{meal.meal_type}' pour le user {user_id}: {e}")
        raise


def get_meal_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Meal.query.filter(Meal.user_id == user_id, Meal.entry_date >= start_date, Meal.entry_date <= end_date).order_by(Meal.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_meal_entry] Aucune entrée trouvée pour l’utilisateur {user_id} ({range_type}).")
            return []
        app.logger.info(f"[BACK][services/data_services][get_meal_entry] {len(entries)} entrées trouvées pour l'utilisateur {user_id}, {range_type} → {start_date} à {end_date}") # type: ignore
        result = []
        for entry in entries: # type: ignore
            meal_dict = entry.to_dict()
            result.append(meal_dict)
        return result

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_meal_entry] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_meal_entry] Erreur inattendue : {e}")
        raise


def update_meal_entry(user_id: str, entry_id: str, new_data: dict):
    try:
        entry = Meal.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/data_service.py][update_meal_entry] Aucune entrée trouvée pour cet utilisateur")
            return None
        validated = validate_meal_data(new_data)
        entry.description = validated.description
        entry.meal_type = validated.meal_type
        entry.save()
        app.logger.info(f"[BACK][services/data_service.py][update_meal_entry] Entrée {entry_id} mise à jour du repas {entry.description} pour le {entry.meal_type}, pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_meal_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_meal_entry] Erreur inattendue : {e}")
        raise


def delete_meal_entry(entry_id: str, user_id: str):
    """Supprimer une mesure de l'utilisateur"""
    try:
        entry = Meal.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_meal_entry] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_meal_entry] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_meal_entry] Erreur inattendue pour user {user_id}, entry {entry_id} : {e}")
        raise


# ---------------------------------------------------------------------- Mood
def validate_mood_data(data: dict) -> Mood:
    """Valide les données du modèle Mood via les setters."""
    try:
        mood = Mood()
        mood.description = data.get("description")
        app.logger.info(f"[BACK][services/data_service.py][validate_mood_data] Les valeurs {mood.description} pour le mood sont valides")
        return mood

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_mood_data] Erreur de validation du mood : {str(e)}")
        raise


def create_mood_entry(user_id: str, data: dict):
    """Crée une nouvelle entrée d’humeur pour un utilisateur donné."""
    try:
        mood = validate_mood_data(data)
        mood.user_id = user_id
        mood.save()
        app.logger.info(f"[BACK][services/data_service.py][create_mood_entry] L’humeur '{mood.description}' a été enregistrée pour l’utilisateur {user_id}")
        return mood.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_mood_entry] Erreur lors de la création de l’humeur pour user {user_id} : {e}")
        raise


def get_mood_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    """Récupère les entrées d’humeur sur une période donnée."""
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Mood.query.filter(Mood.user_id == user_id, Mood.entry_date >= start_date, Mood.entry_date <= end_date).order_by(Mood.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_mood_entry()] Aucune humeur trouvée pour user {user_id} ({range_type})")
            return []
        app.logger.info(f"[BACK][services/data_service.py][get_mood_entry()] {len(entries)} humeurs récupérées pour user {user_id}, période {range_type} → {start_date} à {end_date}")
        result = []
        for entry in entries: # type: ignore
            mood_dict = entry.to_dict()
            result.append(mood_dict)
        return result

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][get_mood_entry()] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_mood_entry()] Erreur inattendue : {e}")
        raise


def update_mood_entry(user_id: str, entry_id: str, new_data: dict):
    """Met à jour une entrée d’humeur existante."""
    try:
        entry = Mood.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][update_mood_entry()] Aucune entrée trouvée pour user {user_id} (id: {entry_id})")
            return None
        validated = validate_mood_data(new_data)
        entry.description = validated.description
        entry.save()
        app.logger.info(f"[BACK][services/data_service.py][update_mood_entry()] Entrée {entry_id} mise à jour avec la valeur '{entry.description}' pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_mood_entry()] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_mood_entry()] Erreur inattendue : {e}")
        raise


def delete_mood_entry(entry_id: str, user_id: str):
    """Supprime une entrée d’humeur."""
    try:
        entry = Mood.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_mood_entry()] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_mood_entry()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id, "status": "deleted"}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_mood_entry()] Erreur inattendue pour user {user_id}, entry {entry_id} : {e}")
        raise


# ---------------------------------------------------------------------- Medication
def validate_medication_data(data: dict) -> Medication:
    """Valide les données pour la création ou la mise à jour d’un médicament."""
    try:
        medication = Medication()
        medication.name = data.get("name")
        medication.stock = data.get("stock")
        medication.dose = data.get("dose")
        medication.frequency = data.get("frequency")
        app.logger.info(f"[BACK][services/data_service.py][validate_medication_data] Le médicament {medication.name}, d'une quantité de {medication.stock} pour une dose de {medication.dose} tout les {medication.frequency} valides")
        return medication

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_medication_data] Erreur de validation : {str(e)}")
        raise


def create_medication_entry(user_id: str, data: dict):
    """Crée un nouveau médicament pour l’utilisateur."""
    try:
        medication = validate_medication_data(data)
        medication.user_id = user_id
        medication.save()
        app.logger.info(f"[BACK][services/data_service.py][create_medication_entry()] Médicament '{medication.name}' ajouté pour user {user_id}, dose : {medication.dose} mg, stock : {medication.stock} mg")
        return medication.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_medication_entry()] Erreur lors de la création : {e}")
        raise


def get_medication_entry(user_id: str) -> list[dict]:
    """Récupère tous les médicaments enregistrés pour un utilisateur."""
    try:
        entries = (Medication.query.filter_by(user_id=user_id).order_by(Medication.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_medication_entry()] Aucun médicament trouvé pour user {user_id}")
            return []
        app.logger.info(f"[BACK][services/data_service.py][get_medication_entry()] {len(entries)} médicaments trouvés pour user {user_id}")
        result = []
        for entry in entries: # type: ignore
            medication_dict = entry.to_dict()
            result.append(medication_dict)
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_medication_entry()] Erreur inattendue : {e}")
        raise


def update_medication_entry(user_id: str, entry_id: str, new_data: dict):
    """Met à jour un médicament existant."""
    try:
        entry = Medication.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][update_medication_entry] Aucun médicament trouvé pour user {user_id}")
            return None
        app.logger.info(f"[BACK][services/data_service.py][update_medication_entry] Le médicament : {entry.name} à été trouvé")
        validated = validate_medication_data(new_data)
        entry.name = validated.name
        entry.dose = validated.dose
        entry.stock = validated.stock
        entry.frequency = validated.frequency
        entry.save()
        app.logger.info(f"[BACK][services/data_service.py][update_medication_entry()] Médicament {entry_id} mis à jour pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_medication_entry()] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_medication_entry()] Erreur inattendue : {e}")
        raise


def delete_medication_entry(entry_id: str, user_id: str):
    """Supprime un médicament de la base."""
    try:
        entry = Medication.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_medication_entry()] Aucun médicament trouvé pour user {user_id}")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_medication_entry()] Médicament {entry_id} supprimé pour user {user_id}")
        return {"deleted_entry_id": entry_id, "status": "deleted"}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_medication_entry()] Erreur inattendue : {e}")
        raise


def take_medication_dose(user_id: str, entry_id: str):
    """
    Enregistre une prise de médicament → soustrait une dose du stock
    Déclenche une alerte si le stock devient faible
    """
    try:
        entry = Medication.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][take_medication_dose()] Aucun médicament trouvé pour user {user_id}")
            return None
        old_stock = entry.stock
        entry.take_dose()
        new_stock = entry.stock
        app.logger.info(f"[BACK][services/data_service.py][take_medication_dose()] Prise enregistrée pour {entry.name} ({entry.dose} mg). Stock : {old_stock} mg → {new_stock} mg")
        if entry.alert_low_stock():
            app.logger.warning(f"[BACK][services/data_service.py][take_medication_dose()] Stock faible pour {entry.name} ({entry.stock} mg restants, seuil : {entry._alert_threshold} mg)")
        entry.save()
        return entry.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][take_medication_dose()] Erreur inattendue lors de la prise : {e}")
        raise


# ---------------------------------------------------------------------- HealthProfessional
def validate_health_professional_data(data: dict) -> HealthProfessional:
    try:
        pro = HealthProfessional()
        pro.fullname = data.get("fullname")
        pro.speciality = data.get("speciality")
        pro.phone = data.get("phone")
        app.logger.info(f"[BACK][services/data_service.py][validate_health_professional_data] Le {pro.fullname} qui est {pro.speciality} joignable au {pro.phone} est valide")
        return pro

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_health_professional_data] Erreur de validation du professionnel de santé : {str(e)}")
        raise


def create_health_professional_entry(user_id, data):
    try:
        pro = validate_health_professional_data(data)
        pro.user_id = user_id
        pro.save()
        app.logger.info(f"[BACK][services/data_service.py][create_health_professional_entry] Professionnel {pro.fullname} ({pro.speciality}) enregistré pour le user {user_id}")
        return pro.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_health_professional_entry] Erreur lors de la création : {e}")
        raise


def get_health_professional_entries(user_id: str) -> list[dict]:
    try:
        entries = (HealthProfessional.query.filter_by(user_id=user_id).order_by(HealthProfessional.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_health_professional_entries] Aucun professionnel trouvé pour l’utilisateur {user_id}.")
            return []
        result = []
        for entry in entries: # type: ignore
            pros_dict = entry.to_dict()
            result.append(pros_dict)
        app.logger.info(f"[BACK][services/data_service.py][get_health_professional_entries] {len(result)} professionnels récupérés pour l’utilisateur {user_id}.")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_health_professional_entries] Erreur inattendue : {e}")
        raise


def get_health_professional_with_notes(user_id: str, professional_id: str) -> dict:
    """Récupère un professionnel de santé et toutes ses notes associées, triées par date décroissante"""
    try:
        professional = HealthProfessional.query.filter_by(id=professional_id, user_id=user_id).first()
        if not professional:
            app.logger.info(f"[BACK][services/data_service.py][get_health_professional_with_notes] Aucun professionnel trouvé pour l’utilisateur {user_id}")
            return {}
        notes = sorted(professional.notes, key=lambda n: n.entry_date, reverse=True)
        result = professional.to_dict()
        result["notes"] = []
        for note in notes:
            note_to_dict = note.to_dict()
            result.append(note_to_dict)
        app.logger.info(f"[BACK][services/data_service.py][get_health_professional_with_notes] {len(notes)} notes récupérées pour le pro {professional_id} (user {user_id})")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_health_professional_with_notes] Erreur inattendue : {e}")
        raise


def update_health_professional_entry(user_id: str, entry_id: str, new_data: dict):
    try:
        entry = HealthProfessional.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/data_service.py][update_health_professional_entry] Aucune entrée trouvée pour cet utilisateur.")
            return None
        if "fullname" in new_data:
            validated_fullname = validate_health_professional_data({"fullname": new_data["fullname"], "speciality": entry.speciality, "phone": entry.phone})
            entry.fullname = validated_fullname.fullname
        if "speciality" in new_data:
            validated_speciality = validate_health_professional_data({"speciality": new_data["speciality"], "fullname": entry.fullname, "phone": entry.phone})
            entry.speciality = validated_speciality.speciality
        if "phone" in new_data:
            validated_phone = validate_health_professional_data({"phone": new_data["phone"], "speciality": entry.speciality, "fullname": entry.fullname})
            entry.phone = validated_phone.phone
        entry.save()
        app.logger.info(f"[BACK][services/data_service.py][update_health_professional_entry] Entrée {entry_id} mise à jour ({entry.fullname}, {entry.speciality}) pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_health_professional_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_health_professional_entry] Erreur inattendue : {e}")
        raise


def delete_health_professional_entry(entry_id: str, user_id: str):
    """Supprimer un professionnel de santé"""
    try:
        entry = HealthProfessional.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_health_professional_entry] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_health_professional_entry] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_health_professional_entry] Erreur inattendue : {e}")
        raise


# ---------------------------------------------------------------------- Note
def validate_note_data(data: dict) -> Note:
    try:
        note = Note()
        note.title = data.get("title")
        note.content = data.get("content")
        app.logger.info(f"[BACK][services/data_service.py][validate_note_data] Le titre: {note.title} et le contenu: {note.content} de la note sont valides")
        return note

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_note_data] Erreur de validation des données de la note : {str(e)}")
        raise


def create_note_entry(user_id: str, health_professional_id: str, data: dict) -> Note:
    try:
        note = validate_note_data(data)
        note.user_id = user_id
        note.health_professional_id = health_professional_id
        note.save()
        app.logger.info(f"[BACK][services/data_service.py][create_note_entry] Nouvelle note '{note.title}' créée pour user {user_id}, professionnel {health_professional_id}")
        return note

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_note_entry] Erreur lors de la création de la note : {e}")
        raise


def get_note_entries(user_id: str, health_professional_id: str) -> list[dict]:
    try:
        entries = (Note.query.filter_by(user_id=user_id, health_professional_id=health_professional_id).order_by(Note.entry_date.desc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/data_service.py][get_note_entries] Aucune note trouvée pour user {user_id} et professionnel {health_professional_id}")
            return []
        result = []
        for entry in entries:
            entry_dict = entry.to_dict()
            result.append(entry_dict)
        app.logger.info(f"[BACK][services/data_service.py][get_note_entries] {len(result)} notes récupérées pour user {user_id}, professionnel {health_professional_id}")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_note_entries] Erreur inattendue : {e}")
        raise


def update_note_entry(user_id: str, entry_id: str, new_data: dict):
    try:
        entry = Note.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/data_service.py][update_note_entry] Aucune note trouvée pour cet utilisateur.")
            return None
        if "title" in new_data:
            validated_title = validate_note_data({"title": new_data["title"], "content": entry.content})
            entry.title = validated_title.title
        if "content" in new_data:
            validated_content = validate_note_data({"content": new_data["content"], "title": entry.title})
            entry.content = validated_content.content
        entry.save()
        app.logger.info(f"[BACK][services/data_service.py][update_note_entry] Note {entry_id} mise à jour : '{entry.title}' pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_note_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_note_entry] Erreur inattendue : {e}")
        raise


def delete_note_entry(entry_id: str, user_id: str):
    """Supprime une note"""
    try:
        entry = Note.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/data_service.py][delete_note_entry] Aucune note trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_note_entry] Note {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_note_entry] Erreur inattendue : {e}")
        raise


# ------------------------------------------------------------------- ForumPost
def validate_forum_post_data(data: dict) -> ForumPost:
    try:
        forum_post = ForumPost()
        forum_post.title = data.get("title")
        forum_post.content = data.get("content")
        app.logger.info(f"[BACK][services/data_service.py][validate_forum_post_data] Le titre: {forum_post.title}, le contenu: {forum_post.content} et son nombre de likes: {forum_post.likes} du post sont valides")
        return forum_post

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_forum_post_data] Erreur de validation des données du post : {str(e)}")
        raise


def create_forum_post_entry(user_id, data):
    """Crée un nouveau post dans le forum."""
    try:
        forum_post = validate_forum_post_data(data)
        forum_post.user_id = user_id
        forum_post.save()
        app.logger.info(f"[BACK][services/data_service.py][create_forum_post_entry] Post {forum_post.title} créé par user {user_id}")
        return forum_post.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_forum_post_entry] Erreur lors de la création du post sur le forum : {e}")
        raise


def get_all_forum_posts(sort_by="recent"):
    """Retourne tous les posts triés par date ou popularité."""
    try:
        if sort_by == "popular":
            posts = ForumPost.query.order_by(ForumPost._likes.desc(), ForumPost.created_at.desc()).all() # type: ignore
        else:
            posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
        result = []
        for post in posts:
            posts_dict = post.to_dict()
            result.append(posts_dict)
        app.logger.info("[BACK][services/data_service.py][get_all_forum_posts] Liste des posts renvoyée")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_all_forum_posts] Erreur inattendue : {e}")
        raise


def get_forum_post_by_id(post_id):
    """Retourne un post et ses commentaires."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][get_forum_post_by_id] Post {post_id} introuvable")
            return None
        post_data = post.to_dict()
        post_data["comments"] = []
        for comment in post.comments:
            comment_dict = comment.to_dict()
            post_data["comments"].append(comment_dict)
            app.logger.info(f"[BACK][services/data_service.py][get_forum_post_by_id] Commentaire ajouté → {comment_dict.get('id')}")
        app.logger.info(f"[BACK][services/data_service.py][get_forum_post_by_id] Post {post_id} récupéré avec ses commentaires")
        return post_data

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_forum_post_by_id] Erreur inattendue : {e}")
        raise


def update_forum_post_entry(post_id: str, new_data: dict, user_id: str):
    """Modifie un post existant (seulement par son auteur)."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.info("[BACK][services/data_service.py][update_forum_post_entry] Aucune entrée trouvée pour cet utilisateur.")
            return None, 404
        if post.user_id != user_id:
            app.logger.info("[BACK][services/data_service.py][update_forum_post_entry] Utilisateur non autorisé à modifier ce post")
            return None, 403
        if "title" in new_data:
            validated_title = validate_forum_post_data({"title": new_data["title"], "content": post.content})
            post.title = validated_title.title
        if "content" in new_data:
            validated_content = validate_forum_post_data({"content": new_data["content"], "title": post.title})
            post.content = validated_content.content
        post.save()
        app.logger.info(f"[BACK][services/data_service.py][update_forum_post_entry] Post {post.id} mis à jour par user {user_id}")
        return post.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/data_service.py][update_forum_post_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_forum_post_entry] Erreur inattendue : {e}")
        raise


def delete_forum_post(post_id: str, user_id: str):
    """Supprime un post (auteur uniquement)."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.info(f"[BACK][services/data_service.py][delete_forum_post] Aucune entrée trouvée pour user {user_id} (entry_id: {post_id})")
            return None
        if post.user_id != user_id:
            app.logger.info("[BACK][services/data_service.py][delete_forum_post] Utilisateur non autorisé à supprimer ce post")
            return None
        post.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_forum_post] Post {post_id} supprimé par user {user_id}")
        return {"deleted_forum_post_id": post_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_forum_post] Erreur inattendue : {e}")
        raise


def toggle_like_forum_post(post_id: str, user_id: str):
    """Ajoute ou retire un like sur un post."""
    try:
        user = User.query.get(user_id)
        if not user:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_forum_post()] Utilisateur {user_id} introuvable")
            return None
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_forum_post()] Post {post_id} introuvable")
            return None
        if post.user_id == user_id:
            app.logger.info(f"[BACK][services/data_service.py][toggle_like_forum_post()] User {user_id} a tenté de liker son propre post {post_id}")
            return None
        if post in user.liked_posts:
            user.liked_posts.remove(post)
            post.likes -= 1
            message = "Like retiré"
        else:
            user.liked_posts.append(post)
            post.increment_likes()
            message = "Post liké"
        db.session.commit()
        app.logger.info(f"[BACK][services/data_service.py][toggle_like_forum_post()] User {user_id} → {message} post {post_id}")
        return {"post_id": post_id, "likes": post.likes, "message": message}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][toggle_like_forum_post()] Erreur inattendue : {e}")
        raise


# --------------------------------------------------------------------- Comment
def validate_comment_data(data: dict) -> Comment:
    try:
        comment = Comment()
        comment.content = data.get("content")
        comment.likes = data.get("likes")
        app.logger.info(f"[BACK][services/data_service.py][validate_comment_data] Le contenu {comment.content} et les likes {comment.likes} du commentaire sont valides")
        return comment

    except (ValueError, TypeError) as e:
        app.logger.error(f"Erreur de validation du commentaire: {str(e)}")
        raise


def create_comment_entry(post_id: str, user_id: str, data: dict) -> Comment:
    """Crée un nouveau commentaire associé à un post du forum."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][create_comment_entry] Post {post_id} introuvable")
            return None # type: ignore
        validated_comment = validate_comment_data(data)
        validated_comment.user_id = user_id
        validated_comment.post_id = post_id
        validated_comment.save()
        app.logger.info(f"[BACK][services/data_service.py][create_comment_entry] Commentaire {validated_comment.id} créé sur post {post_id} par user {user_id}")
        return validated_comment.to_dict() # type: ignore

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_comment_entry] Erreur inattendue : {e}")
        raise


def get_comments_by_post(post_id: str):
    """Récupère tous les commentaires d’un post."""
    try:
        post = ForumPost.query.get(post_id)
        if not post:
            app.logger.error(f"[BACK][services/data_service.py][get_comments_by_post] Post {post_id} introuvable")
            return None
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
        result = []
        for comment in comments:
            comment_dict = comment.to_dict()
            result.append(comment_dict)
            app.logger.debug(f"[BACK][services/data_service.py][get_comments_by_post] Commentaire ajouté → {comment_dict.get('id')}")
        app.logger.info(f"[BACK][services/data_service.py][get_comments_by_post] {len(result)} commentaires récupérés pour le post {post_id}")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_comments_by_post] Erreur inattendue : {e}")
        raise


def update_comment_entry(comment_id: str, user_id: str, data: dict):
    """Modifie un commentaire existant (auteur uniquement)."""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][update_comment_entry] Commentaire {comment_id} introuvable")
            return None
        if comment.user_id != user_id:
            app.logger.info(f"[BACK][services/data_service.py][update_comment_entry] User {user_id} non autorisé à modifier ce commentaire")
            return None
        validated_comment = validate_comment_data(data)
        comment.content = validated_comment.content
        comment.save()
        app.logger.info(f"[BACK][services/data_service.py][update_comment_entry] Commentaire {comment.id} mis à jour par user {user_id}")
        return comment.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_comment_entry] Erreur inattendue : {e}")
        raise


def delete_comment_entry(comment_id: str, user_id: str):
    """Supprime un commentaire (auteur uniquement)."""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][delete_comment_entry] Commentaire {comment_id} introuvable")
            return None
        if comment.user_id != user_id:
            app.logger.info(f"[BACK][services/data_service.py][delete_comment_entry] User {user_id} non autorisé à supprimer ce commentaire")
            return None
        comment.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_comment_entry] Commentaire {comment_id} supprimé par user {user_id}")
        return {"deleted_comment_id": comment_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_comment_entry] Erreur inattendue : {e}")
        raise


def toggle_like_comment(comment_id: str, user_id: str):
    """Ajoute ou retire un like sur un commentaire (toggle)."""
    try:
        user = User.query.get(user_id)
        if not user:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Utilisateur {user_id} introuvable")
            return None
        comment = Comment.query.get(comment_id)
        if not comment:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Commentaire {comment_id} introuvable")
            return None
        if comment.user_id == user_id:
            app.logger.info(f"[BACK][services/data_service.py][toggle_like_comment] User {user_id} a tenté de liker son propre commentaire {comment_id}")
            return None
        if comment in user.liked_comments:
            user.liked_comments.remove(comment)
            comment.likes -= 1
            message = "Like retiré"
        else:
            user.liked_comments.append(comment)
            comment.increment_likes()
            message = "Commentaire liké"
        db.session.commit()
        app.logger.info(f"[BACK][services/data_service.py][toggle_like_comment] User {user_id} → {message} sur commentaire {comment_id}")
        return {"comment_id": comment_id, "likes": comment.likes, "message": message}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][toggle_like_comment] Erreur inattendue : {e}")
        raise


# --------------------------------------------------------------------- Article
def validate_article_data(data: dict) -> Article:
    try:
        article = Article()
        article.title = data.get("title")
        article.content = data.get("content")
        article.likes = data.get("likes")
        app.logger.info(f"[BACK][services/data_service.py][validate_article_data] Données de l'article {article.title} validées")
        return article

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/data_service.py][validate_article_data] Erreur de validation : {str(e)}")
        raise


def create_article_entry(data, user_id) -> Article:
    """Crée un nouvel article (admin uniquement)."""
    try:
        user = User.query.get(user_id)
        if not user:
            app.logger.error(f"[BACK][services/data_service.py][create_article_entry] User {user_id} introuvable")
            return None # type: ignore
        if user.role != "admin":
            app.logger.warning(f"[BACK][services/data_service.py][create_article_entry] User {user_id} non autorisé à créer un article")
            return None # type: ignore
        article = validate_article_data(data)
        article.user_id = user_id
        article.save()
        app.logger.info(f"[BACK][services/data_service.py][create_article_entry] Article {article.title} créé par admin {user_id}")
        return article.to_dict() # type: ignore

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][create_article_entry] Erreur inattendue : {e}")
        raise


def get_all_articles(sort_by: str = "recent"):
    """Récupère tous les articles (triés par date ou popularité)."""
    try:
        if sort_by == "popular":
            articles = Article.query.order_by(Article._likes.desc(), Article.created_at.desc()).all() #type: ignore
        else:
            articles = Article.query.order_by(Article.created_at.desc()).all()
        result = []
        for article in articles:
            article_dict = article.to_dict()
            result.append(article_dict)
            app.logger.debug(f"[BACK][services/data_service.py][get_all_articles] Article ajouté → {article_dict.get('id')}")
        app.logger.info(f"[BACK][services/data_service.py][get_all_articles] {len(result)} articles récupérés (tri={sort_by})")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_all_articles] Erreur inattendue : {e}")
        raise


def get_article_by_id(article_id: str):
    """Récupère un article précis."""
    try:
        article = Article.query.get(article_id)
        if not article:
            app.logger.error(f"[BACK][services/data_service.py][get_article_by_id] Article {article_id} introuvable")
            return None
        app.logger.info(f"[BACK][services/data_service.py][get_article_by_id] Article {article_id} récupéré")
        return article.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][get_article_by_id] Erreur inattendue : {e}")
        raise


def update_article_entry(article_id: str, user_id: str, data: dict):
    """Met à jour un article (admin uniquement)."""
    try:
        user = User.query.get(user_id)
        article = Article.query.get(article_id)
        if not article:
            app.logger.error(f"[BACK][services/data_service.py][update_article_entry] Article {article_id} introuvable")
            return None
        if not user or user.role != "admin":
            app.logger.warning(f"[BACK][services/data_service.py][update_article_entry] User {user_id} non autorisé à modifier un article")
            return None
        validated_article = validate_article_data(data)
        article.title = validated_article.title
        article.content = validated_article.content
        article.save()
        app.logger.info(f"[BACK][services/data_service.py][update_article_entry] Article {article.id} mis à jour par admin {user_id}")
        return article.to_dict()

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_article_entry] Erreur inattendue : {e}")
        raise


def delete_article_entry(article_id: str, user_id: str):
    """Supprime un article (admin uniquement)."""
    try:
        user = User.query.get(user_id)
        article = Article.query.get(article_id)
        if not article:
            app.logger.error(f"[BACK][services/data_service.py][delete_article_entry] Article {article_id} introuvable")
            return None
        if not user or user.role != "admin":
            app.logger.warning(f"[BACK][services/data_service.py][delete_article_entry] User {user_id} non autorisé à supprimer un article")
            return None
        article.delete()
        app.logger.info(f"[BACK][services/data_service.py][delete_article_entry] Article {article_id} supprimé par admin {user_id}")
        return {"deleted_article_id": article_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][delete_article_entry] Erreur inattendue : {e}")
        raise


def toggle_like_article(article_id: str, user_id: str):
    """Ajoute ou retire un like sur un article."""
    try:
        user = User.query.get(user_id)
        article = Article.query.get(article_id)
        if not user:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_article] Utilisateur {user_id} introuvable")
            return None
        if not article:
            app.logger.error(f"[BACK][services/data_service.py][toggle_like_article] Article {article_id} introuvable")
            return None
        if article.user_id == user_id:
            app.logger.info(f"[BACK][services/data_service.py][toggle_like_article] User {user_id} a tenté de liker son propre article {article_id}")
            return None
        if article in user.liked_articles:
            user.liked_articles.remove(article)
            article.likes -= 1
            message = "Like retiré"
        else:
            user.liked_articles.append(article)
            article.increment_likes()
            message = "Article liké"
        db.session.commit()
        app.logger.info(f"[BACK][services/data_service.py][toggle_like_article] User {user_id} → {message} sur article {article_id}")
        return {"article_id": article_id, "likes": article.likes, "message": message}

    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][toggle_like_article] Erreur inattendue : {e}")
        raise
