from flask import current_app as app
from app.models import Note


def validate_note_data(data: dict) -> Note:
    try:
        note = Note()
        note.title = data.get("title")
        note.content = data.get("content")
        app.logger.info(f"[BACK][services/note_service.py][validate_note_data] Le titre: {note.title} et le contenu: {note.content} de la note sont valides")
        return note

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][services/note_service.py][validate_note_data] Erreur de validation des données de la note : {str(e)}")
        raise


def create_note_entry(user_id: str, health_professional_id: str, data: dict) -> Note:
    try:
        note = validate_note_data(data)
        note.user_id = user_id
        note.health_professional_id = health_professional_id
        note.save()
        app.logger.info(f"[BACK][services/note_service.py][create_note_entry] Nouvelle note '{note.title}' créée pour user {user_id}, professionnel {health_professional_id}")
        return note

    except Exception as e:
        app.logger.error(f"[BACK][services/note_service.py][create_note_entry] Erreur lors de la création de la note : {e}")
        raise


def get_note_entries(user_id: str, health_professional_id: str) -> list[dict]:
    try:
        entries = (Note.query.filter_by(user_id=user_id, health_professional_id=health_professional_id).order_by(Note.entry_date.desc()).all())
        if not entries:
            app.logger.info(f"[BACK][services/note_service.py][get_note_entries] Aucune note trouvée pour user {user_id} et professionnel {health_professional_id}")
            return []
        result = []
        for entry in entries:
            entry_dict = entry.to_dict()
            result.append(entry_dict)
        app.logger.info(f"[BACK][services/note_service.py][get_note_entries] {len(result)} notes récupérées pour user {user_id}, professionnel {health_professional_id}")
        return result

    except Exception as e:
        app.logger.error(f"[BACK][services/note_service.py][get_note_entries] Erreur inattendue : {e}")
        raise


def update_note_entry(user_id: str, entry_id: str, new_data: dict):
    try:
        entry = Note.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info("[BACK][services/note_service.py][update_note_entry] Aucune note trouvée pour cet utilisateur.")
            return None
        if "title" in new_data:
            validated_title = validate_note_data({"title": new_data["title"], "content": entry.content})
            entry.title = validated_title.title
        if "content" in new_data:
            validated_content = validate_note_data({"content": new_data["content"], "title": entry.title})
            entry.content = validated_content.content
        entry.save()
        app.logger.info(f"[BACK][services/note_service.py][update_note_entry] Note {entry_id} mise à jour : '{entry.title}' pour user {user_id}")
        return entry.to_dict()

    except ValueError as e:
        app.logger.error(f"[BACK][services/note_service.py][update_note_entry] Erreur de validation : {e}")
        raise
    except Exception as e:
        app.logger.error(f"[BACK][services/note_service.py][update_note_entry] Erreur inattendue : {e}")
        raise


def delete_note_entry(entry_id: str, user_id: str):
    """Supprime une note"""
    try:
        entry = Note.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            app.logger.info(f"[BACK][services/note_service.py][delete_note_entry] Aucune note trouvée pour user {user_id} (entry_id: {entry_id})")
            return None
        entry.delete()
        app.logger.info(f"[BACK][services/note_service.py][delete_note_entry] Note {entry_id} supprimée avec succès pour user {user_id}")
        return {"deleted_entry_id": entry_id}

    except Exception as e:
        app.logger.error(f"[BACK][services/note_service.py][delete_note_entry] Erreur inattendue : {e}")
        raise
