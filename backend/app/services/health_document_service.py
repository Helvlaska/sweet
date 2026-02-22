from flask import current_app as app
from werkzeug.utils import secure_filename
from app.models import HealthDocument
from app import db


def create_document_entry(user_id: str, health_professional_id: str, filename : str, file_data: str) -> HealthDocument:
    try:
        # Limite backend : 10 documents / pro
        count = HealthDocument.query.filter_by(
            user_id=user_id,
            health_professional_id=health_professional_id
        ).count()

        if count >= 10:
            app.logger.error("[BACK][health_document_service][create_document_entry] Limite de 10 documents atteinte pour ce professionnel")
            raise ValueError("Limite de 10 documents par professionnel atteinte")

        document = HealthDocument()
        document.filename = secure_filename(filename)
        document.file = file_data
        document.user_id = user_id
        document.health_professional_id = health_professional_id

        document.save()

        app.logger.info(f"[BACK][health_document_service][create_document_entry] Document '{document.filename}' créé pour user={user_id}, pro={health_professional_id}")

        return document

    except ValueError as e:
        app.logger.error(f"[BACK][health_document_service][create_document_entry] Erreur validation : {e}")
        raise

    except Exception as e:
        app.logger.error(f"[BACK][health_document_service][create_document_entry] Erreur inattendue : {e}")
        raise


def get_documents_by_pro(user_id: str, health_professional_id: str) -> list[dict]:
    try:
        documents = (
            HealthDocument.query
            .filter_by(user_id=user_id, health_professional_id=health_professional_id)
            .order_by(HealthDocument.created_at.desc())
            .all()
        )

        result = [doc.to_dict() for doc in documents]

        app.logger.info(
            "[BACK][health_document_service][get_documents_by_pro] "
            f"{len(result)} documents récupérés pour user={user_id}, pro={health_professional_id}"
        )

        return result

    except Exception as e:
        app.logger.error(
            "[BACK][health_document_service][get_documents_by_pro] "
            f"Erreur récupération documents : {e}"
        )
        raise


def get_all_documents_by_user(user_id: str) -> list[dict]:
    try:
        documents = (
            HealthDocument.query
            .filter_by(user_id=user_id)
            .order_by(HealthDocument.created_at.desc())
            .all()
        )

        result = [doc.to_dict() for doc in documents]

        app.logger.info(
            "[BACK][health_document_service][get_all_documents_by_user] "
            f"{len(result)} documents récupérés pour user={user_id}"
        )

        return result

    except Exception as e:
        app.logger.error(
            "[BACK][health_document_service][get_all_documents_by_user] "
            f"Erreur récupération globale documents : {e}"
        )
        raise


def update_document_entry(user_id: str, document_id: str, new_data: dict):
    try:
        document = HealthDocument.query.filter_by(
            id=document_id,
            user_id=user_id
        ).first()

        if not document:
            app.logger.info(
                "[BACK][health_document_service][update_document_entry] "
                f"Aucun document trouvé (user={user_id}, document={document_id})"
            )
            return None

        if "filename" in new_data:
            document.filename = new_data["filename"]

        if "file" in new_data:
            document.file = new_data["file"]

        document.save()

        app.logger.info(
            "[BACK][health_document_service][update_document_entry] "
            f"Document {document_id} mis à jour"
        )

        return document.to_dict()

    except ValueError as e:
        app.logger.error(
            "[BACK][health_document_service][update_document_entry] "
            f"Erreur validation : {e}"
        )
        raise

    except Exception as e:
        app.logger.error(
            "[BACK][health_document_service][update_document_entry] "
            f"Erreur inattendue : {e}"
        )
        raise


def delete_document_entry(user_id: str, document_id: str):
    try:
        document = HealthDocument.query.filter_by(
            id=document_id,
            user_id=user_id
        ).first()

        if not document:
            app.logger.info(
                "[BACK][health_document_service][delete_document_entry] "
                f"Aucun document trouvé (user={user_id}, document={document_id})"
            )
            return None

        document.delete()

        app.logger.info(
            "[BACK][health_document_service][delete_document_entry] "
            f"Document {document_id} supprimé"
        )

        return {"deleted_document_id": document_id}

    except Exception as e:
        app.logger.error(
            "[BACK][health_document_service][delete_document_entry] "
            f"Erreur suppression document : {e}"
        )
        raise
