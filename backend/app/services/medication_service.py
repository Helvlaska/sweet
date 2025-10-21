from flask import current_app as app
from app.models import Medication
from app.utils import timelaps


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
