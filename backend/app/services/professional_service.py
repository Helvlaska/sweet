"""
[BACK][services/professional_service.py]

Service layer — health professional business logic.
Called exclusively from professional_routes.py.

Exposed functions:
  validate_health_professional_data(data)
  create_health_professional_entry(user_id, data)
  get_health_professional_entries(user_id)
  get_health_professional_with_details(user_id, professional_id)
  update_health_professional_entry(user_id, entry_id, new_data)
  delete_health_professional_entry(entry_id, user_id)

Unexposed (reserved for future use):
  get_health_professional_with_notes(user_id, professional_id)
"""


from flask import current_app as app
from app.models import HealthProfessional
from app.services import health_document_service


def validate_health_professional_data(data: dict) -> HealthProfessional:
    """Validate and return a HealthProfessional instance."""
    try:
        if not data:
            app.logger.error("[BACK][services/professional_service.py][validate_health_professional_data] Aucune donnée reçue")
            raise ValueError("Aucune donnée reçue pour la création du professionnel")

        if "fullname" not in data or "speciality" not in data:
            app.logger.error("[BACK][services/professional_service.py][validate_health_professional_data] Champs 'fullname' et 'speciality' requis")
            raise ValueError("Les champs 'fullname' et 'speciality' sont requis")

        pro = HealthProfessional()
        pro.fullname = data.get("fullname")
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

        app.logger.info(f"[BACK][professional_service][validate_health_professional_data] Professionnel validé : {pro.fullname}")
        return pro

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][professional_service][validate_health_professional_data] Erreur validation professionnel : {str(e)}")
        raise


def create_health_professional_entry(user_id: str, data: dict):
    """Create and save a new HealthProfessional entry with optional documents."""
    try:
        pro = validate_health_professional_data(data)
        pro.user_id = user_id
        pro.save()
        documents = data.get("documents", [])

        for document_data in documents:
            health_document_service.create_document_entry(
                user_id=user_id,
                health_professional_id=pro.id,
                filename=document_data.get("filename"),
                file_data=document_data.get("file")
            )

        app.logger.info(f"[BACK][services/professional_service.py][create_health_professional_entry] Professionnel {pro.fullname} créé pour user {user_id}")
        return pro.to_dict()

    except (ValueError, TypeError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/professional_service.py][create_health_professional_entry] Erreur inattendue : {e}")
        raise


def get_health_professional_entries(user_id: str) -> list[dict]:
    """Get a HealthProfessional entry"""
    try:
        entries = (
            HealthProfessional.query
            .filter_by(user_id=user_id)
            .order_by(HealthProfessional.entry_date.asc())
            .all()
        )

        result = [entry.to_dict() for entry in entries]
        app.logger.info(
            f"[BACK][professional_service][get_health_professional_entries] {len(result)} professionnels récupérés pour user {user_id}"
        )
        return result

    except Exception as e:
        app.logger.error(f"[BACK][professional_service][get_health_professional_entries] Erreur inattendue : {e}")
        raise


def get_health_professional_with_notes(user_id: str, professional_id: str) -> dict:
    """Get a HealthProfessional entry with notes"""
    try:
        professional = (
            HealthProfessional.query
            .filter_by(id=professional_id, user_id=user_id)
            .first()
        )

        if not professional:
            app.logger.info(
                "[BACK][professional_service][get_health_professional_with_notes] "
                f"Aucun professionnel trouvé pour user {user_id}"
            )
            return {}

        result = professional.to_dict()
        notes = sorted(
            professional.notes,
            key=lambda n: n.entry_date,
            reverse=True
        )

        result["notes"] = [note.to_dict() for note in notes]
        result["documents"] = health_document_service.get_documents_by_pro(user_id, professional_id)
        app.logger.info(
            "[BACK][professional_service][get_health_professional_with_notes] "
            f"Professionnel {professional_id} récupéré avec {len(notes)} notes"
        )
        return result

    except Exception as e:
        app.logger.error(f"[BACK][professional_service][get_health_professional_with_notes] Erreur inattendue : {e}")
        raise


def get_health_professional_with_details(user_id: str, professional_id: str) -> dict:
    """Get professional with notes & docs"""
    try:
        professional = (
            HealthProfessional.query
            .filter_by(id=professional_id, user_id=user_id)
            .first()
        )

        if not professional:
            app.logger.info(
                f"[BACK][services/professional_service.py][get_health_professional_with_details]"
                f" Aucun professionnel trouvé pour user {user_id}"
            )
            return {}

        notes = sorted(
            professional.notes,
            key=lambda n: n.entry_date,
            reverse=True
        )

        notes_list = []
        for note in notes:
            notes_list.append(note.to_dict())

        documents = health_document_service.get_documents_by_pro(
            user_id,
            professional_id
        )

        result = professional.to_dict()
        result["notes"] = notes_list
        result["documents"] = documents

        app.logger.info(
            f"[BACK][services/professional_service.py][get_health_professional_with_details]"
            f" {len(notes_list)} notes et {len(documents)} documents récupérés"
        )
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/professional_service.py][get_health_professional_with_details] Erreur inattendue : {e}")
        raise


def update_health_professional_entry(user_id: str, entry_id: str, new_data: dict):
    """Update a HealthProfessional entry. Returns None if not found."""
    try:
        entry = (
            HealthProfessional.query
            .filter_by(id=entry_id, user_id=user_id)
            .first()
        )

        if not entry:
            app.logger.info("[BACK][professional_service][update_health_professional_entry] Aucune entrée trouvée.")
            return None

        for field in ["fullname", "speciality", "phone", "email", "address", "postal_code", "city"]:
            if field in new_data:
                setattr(entry, field, new_data[field])

        entry.save()
        documents = new_data.get("documents", [])

        for document_data in documents:
            health_document_service.create_document_entry(
                user_id=user_id,
                health_professional_id=entry.id,
                filename=document_data.get("filename"),
                file_data=document_data.get("file")
            )

        app.logger.info(f"[BACK][professional_service][update_health_professional_entry] Professionnel {entry_id} mis à jour avec {len(documents)} nouveaux documents")
        return entry.to_dict()

    except (ValueError, TypeError):
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/professional_service.py][update_health_professional_entry] Erreur inattendue : {e}")
        raise


def delete_health_professional_entry(entry_id: str, user_id: str):
    """Delete a HealthProfessional entry"""
    try:
        entry = (
            HealthProfessional.query
            .filter_by(id=entry_id, user_id=user_id)
            .first()
        )

        if not entry:
            app.logger.info(f"[BACK][professional_service][delete_health_professional_entry] Aucune entrée trouvée pour user {user_id}")
            return None

        entry.delete()
        app.logger.info(f"[BACK][professional_service][delete_health_professional_entry] Professionnel {entry_id} supprimé")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][professional_service][delete_health_professional_entry] Erreur inattendue : {e}")
        raise
