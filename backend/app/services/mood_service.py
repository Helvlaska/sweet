"""
[BACK][services/mood_service.py]

Service layer — mood business logic.
Called exclusively from mood_routes.py.

Exposed functions:
  validate_mood_data(data)
  create_mood_entry(user_id, data)
  get_mood_entry(user_id, range_type, target_date)
  update_mood_entry(user_id, entry_id, new_data)
  delete_mood_entry(entry_id, user_id)
"""


from flask import current_app as app
from app.models import Mood
from app.utils import timelaps


def validate_mood_data(data: dict) -> Mood:
    """Validate and return a Mood instance."""
    try:
        mood = Mood()
        mood.description = data.get("description")
        app.logger.info(f"[BACK][services/mood_service.py][validate_mood_data] Les valeurs {mood.description} pour le mood sont valides")
        return mood

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/mood_service.py][validate_mood_data] Erreur de validation du mood : {str(e)}")
        raise


def create_mood_entry(user_id: str, data: dict):
    """Create and save a new Mood entry."""
    try:
        mood = validate_mood_data(data)
        mood.user_id = user_id
        mood.save()
        app.logger.info(f"[BACK][services/mood_service.py][create_mood_entry] L’humeur '{mood.description}' a été enregistrée pour l’utilisateur {user_id}")
        return mood.to_dict()

    except (ValueError, TypeError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/mood_service.py][create_mood_entry] Erreur inattendue : {e}")
        raise


def get_mood_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    """Get mood entry"""
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (Mood.query.filter(Mood.user_id == user_id, Mood.entry_date >= start_date, Mood.entry_date <= end_date).order_by(Mood.entry_date.asc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/mood_service.py][get_mood_entry()] Aucune humeur trouvée pour user {user_id} ({range_type})")
            return []

        app.logger.info(f"[BACK][services/mood_service.py][get_mood_entry()] {len(entries)} humeurs récupérées pour user {user_id}, période {range_type} → {start_date} à {end_date}")
        result = []

        for entry in entries: # type: ignore
            mood_dict = entry.to_dict()
            result.append(mood_dict)

        return result

    except ValueError as e:
        app.logger.error(f"[BACK][services/mood_service.py][get_mood_entry()] Erreur de paramètre : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/mood_service.py][get_mood_entry()] Erreur inattendue : {e}")
        raise


def update_mood_entry(user_id: str, entry_id: str, new_data: dict):
    """Update a Mood entry. Returns None if not found."""
    try:
        entry = Mood.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/mood_service.py][update_mood_entry()] Aucune entrée trouvée pour user {user_id} (id: {entry_id})")
            return None

        validated = validate_mood_data(new_data)
        entry.description = validated.description
        entry.save()
        app.logger.info(f"[BACK][services/mood_service.py][update_mood_entry()] Entrée {entry_id} mise à jour avec la valeur '{entry.description}' pour user {user_id}")
        return entry.to_dict()

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/mood_service.py][update_mood_entry()] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/mood_service.py][update_mood_entry()] Erreur inattendue : {e}")
        raise


def delete_mood_entry(entry_id: str, user_id: str):
    """Delete a Mood entry. Returns None if not found."""
    try:
        entry = Mood.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/mood_service.py][delete_mood_entry()] Aucune entrée trouvée pour user {user_id} (entry_id: {entry_id})")
            return None

        entry.delete()
        app.logger.info(f"[BACK][services/mood_service.py][delete_mood_entry()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id, "status": "deleted"}

    except Exception as e:
        app.logger.error(f"[BACK][services/mood_service.py][delete_mood_entry()] Erreur inattendue pour user {user_id}, entry {entry_id} : {e}")
        raise
