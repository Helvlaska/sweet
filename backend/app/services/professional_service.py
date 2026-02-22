from flask import current_app as app
from app.models import HealthProfessional
from app.services import health_document_service


def validate_health_professional_data(data: dict) -> HealthProfessional:
    try:
        pro = HealthProfessional()

        if "fullname" in data:
            pro.fullname = data.get("fullname")

        if "speciality" in data:
            pro.speciality = data.get("speciality")

        if "phone" in data:
            pro.phone = data.get("phone")

        if "email" in data:
            pro.email = data.get("email")

        if "address" in data:
            pro.address = data.get("address")

        if "postal_code" in data:
            pro.postal_code = data.get("postal_code")

        if "city" in data:
            pro.city = data.get("city")

        app.logger.info(
            "[BACK][professional_service][validate_health_professional_data] "
            f"Professionnel validé : {pro.fullname}"
        )

        return pro

    except (ValueError, TypeError) as e:
        app.logger.error(
            "[BACK][professional_service][validate_health_professional_data] "
            f"Erreur validation professionnel : {str(e)}"
        )
        raise


def create_health_professional_entry(user_id: str, data: dict):
    try:
        pro = validate_health_professional_data(data)
        pro.user_id = user_id
        pro.save()

        documents = data.get("documents", [])

        for document_data in documents:
            filename = document_data.get("filename")
            file_data = document_data.get("file")

            health_document_service.create_document_entry(
                user_id=user_id,
                health_professional_id=pro.id,
                filename=filename,
                file_data=file_data
            )

        app.logger.info(
            "[BACK][professional_service][create_health_professional_entry] "
            f"Professionnel {pro.fullname} créé pour user {user_id}"
        )

        return pro.to_dict()

    except Exception as e:
        app.logger.error(
            "[BACK][professional_service][create_health_professional_entry] "
            f"Erreur création professionnel : {e}"
        )
        raise


def get_health_professional_entries(user_id: str) -> list[dict]:
    try:
        entries = (
            HealthProfessional.query
            .filter_by(user_id=user_id)
            .order_by(HealthProfessional.entry_date.asc())
            .all()
        )

        result = [entry.to_dict() for entry in entries]

        app.logger.info(
            "[BACK][professional_service][get_health_professional_entries] "
            f"{len(result)} professionnels récupérés pour user {user_id}"
        )

        return result

    except Exception as e:
        app.logger.error(
            "[BACK][professional_service][get_health_professional_entries] "
            f"Erreur inattendue : {e}"
        )
        raise


def get_health_professional_with_notes(user_id: str, professional_id: str) -> dict:
    try:
        professional = HealthProfessional.query.filter_by(
            id=professional_id,
            user_id=user_id
        ).first()

        if not professional:
            app.logger.info(
                "[BACK][professional_service][get_health_professional_with_notes] "
                f"Aucun professionnel trouvé pour user {user_id}"
            )
            return {}

        result = professional.to_dict()

        # Notes
        notes = sorted(
            professional.notes,
            key=lambda n: n.entry_date,
            reverse=True
        )

        result["notes"] = [note.to_dict() for note in notes]

        # Documents
        result["documents"] = health_document_service.get_documents_by_pro(user_id, professional_id)

        app.logger.info(
            "[BACK][professional_service][get_health_professional_with_notes] "
            f"Professionnel {professional_id} récupéré avec {len(notes)} notes"
        )

        return result

    except Exception as e:
        app.logger.error(
            "[BACK][professional_service][get_health_professional_with_notes] "
            f"Erreur inattendue : {e}"
        )
        raise


def get_health_professional_with_details(user_id: str, professional_id: str) -> dict:
    """Récupère un professionnel avec ses notes et ses documents associés"""
    try:
        professional = HealthProfessional.query.filter_by(
            id=professional_id,
            user_id=user_id
        ).first()

        if not professional:
            app.logger.info(
                f"[BACK][services/professional_service.py]"
                f"[get_health_professional_with_details]"
                f" Aucun professionnel trouvé pour user {user_id}"
            )
            return {}

        # Notes
        notes = sorted(
            professional.notes,
            key=lambda n: n.entry_date,
            reverse=True
        )

        notes_list = []
        for note in notes:
            notes_list.append(note.to_dict())

        # Documents
        documents = health_document_service.get_documents_by_pro(
            user_id,
            professional_id
        )

        result = professional.to_dict()
        result["notes"] = notes_list
        result["documents"] = documents

        app.logger.info(
            f"[BACK][services/professional_service.py]"
            f"[get_health_professional_with_details]"
            f" {len(notes_list)} notes et {len(documents)} documents récupérés"
        )

        return result

    except Exception as e:
        app.logger.error(
            f"[BACK][services/professional_service.py]"
            f"[get_health_professional_with_details]"
            f" Erreur inattendue : {e}"
        )
        raise


def update_health_professional_entry(user_id: str, entry_id: str, new_data: dict):
    try:
        entry = HealthProfessional.query.filter_by(
            id=entry_id,
            user_id=user_id
        ).first()

        if not entry:
            app.logger.info("[BACK][professional_service][update_health_professional_entry] Aucune entrée trouvée.")
            return None

        # Validation ciblée
        for field in ["fullname", "speciality", "phone", "email", "address", "postal_code", "city"]:
            if field in new_data:
                setattr(entry, field, new_data[field])

        entry.save()

        documents = new_data.get("documents", [])

        for document_data in documents:
            filename = document_data.get("filename")
            file_data = document_data.get("file")

            health_document_service.create_document_entry(
                user_id=user_id,
                health_professional_id=entry.id,
                filename=filename,
                file_data=file_data
            )

        app.logger.info(f"[BACK][professional_service][update_health_professional_entry] Professionnel {entry_id} mis à jour avec {len(documents)} nouveaux documents")

        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][professional_service][update_health_professional_entry] Erreur validation : {e}")
        raise

    except Exception as e:
        app.logger.error(f"[BACK][professional_service][update_health_professional_entry] Erreur inattendue : {e}")
        raise


def delete_health_professional_entry(entry_id: str, user_id: str):
    try:
        entry = HealthProfessional.query.filter_by(
            id=entry_id,
            user_id=user_id
        ).first()

        if not entry:
            app.logger.info(
                "[BACK][professional_service][delete_health_professional_entry] "
                f"Aucune entrée trouvée pour user {user_id}"
            )
            return None

        entry.delete()

        app.logger.info(
            "[BACK][professional_service][delete_health_professional_entry] "
            f"Professionnel {entry_id} supprimé"
        )

        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(
            "[BACK][professional_service][delete_health_professional_entry] "
            f"Erreur inattendue : {e}"
        )
        raise
