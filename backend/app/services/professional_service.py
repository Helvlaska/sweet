from flask import current_app as app
from app.models import HealthProfessional


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
