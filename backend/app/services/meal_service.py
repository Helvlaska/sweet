"""
[BACK][services/meal_service.py]

Service layer — meal business logic.
Called exclusively from meal_routes.py.

Exposed functions:
  validate_meal_data(data)
  create_meal_entry(user_id, data)
  get_meal_entry(user_id, range_type, target_date)
  update_meal_entry(user_id, entry_id, new_data)
  delete_meal_entry(entry_id, user_id)
"""


from flask import current_app as app
from app.models import Meal
from app.utils import timelaps


def validate_meal_data(data: dict) -> Meal:
    """Validate and return a Meal instance."""
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
    """Create and save a new Meal entry."""
    try:
        meal = validate_meal_data(data)
        meal.user_id = user_id
        meal.save()
        app.logger.info(f"[BACK][services/data_service.py][create_meal_entry()] Le repas {meal.description} pour le {meal.meal_type} à été enregistrée pour le user {user_id}")
        return meal.to_dict()

    except (ValueError, TypeError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/meal_service.py][create_meal_entry] Erreur inattendue : {e}")
        raise


def get_meal_entry(user_id: str, range_type: str, target_date=None) -> list[dict]:
    """Retrieve meal entries filtered by date range."""
    try:
        start_date, end_date = timelaps.get_time_range(range_type, target_date)
        entries = (
            Meal.query
            .filter(Meal.user_id == user_id, Meal.entry_date >= start_date, Meal.entry_date <= end_date)
            .order_by(Meal.entry_date.asc())
            .all()
        )

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
    """Update a Meal entry. Returns None if not found."""
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

    except (ValueError, TypeError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/data_service.py][update_meal_entry] Erreur inattendue : {e}")
        raise


def delete_meal_entry(entry_id: str, user_id: str):
    """Delete a Meal entry. Returns None if not found."""
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
