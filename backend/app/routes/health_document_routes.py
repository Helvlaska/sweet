from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import health_document_service


document_bp = Blueprint(
    'document',
    __name__,
    url_prefix='/data/health_professionals/<health_professional_id>/documents'
)


@document_bp.route('/', methods=['POST'])
@jwt_required()
def create_document_entry_route(health_professional_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or "documents" not in data:
            return jsonify({"error": "Aucun document fourni."}), 400

        documents = data.get("documents")

        if not isinstance(documents, list) or len(documents) == 0:
            return jsonify({"error": "Liste de documents invalide."}), 400

        created_documents = []

        for doc in documents:
            filename = doc.get("filename")
            file_data = doc.get("file")

            if not filename or not file_data:
                return jsonify({"error": "Document invalide."}), 400

            new_doc = health_document_service.create_document_entry(
                user_id,
                health_professional_id,
                filename,
                file_data
            )

            created_documents.append(new_doc.to_dict())

        app.logger.info(f"[BACK][routes/health_document.py][create_document_entries_route] {len(created_documents)} documents créés pour user {user_id}, pro {health_professional_id}")

        return jsonify(created_documents), 201

    except ValueError as e:
        app.logger.error(f"[BACK][routes/health_document.py][create_document_entries_route] Erreur limite 10, validation model : {e}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        app.logger.error(f"[BACK][routes/health_document.py][create_document_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": "Erreur serveur"}), 500


@document_bp.route('/', methods=['GET'])
@jwt_required()
def get_document_entries_route(health_professional_id):
    try:
        user_id = get_jwt_identity()

        entries = health_document_service.get_documents_by_pro(
            user_id,
            health_professional_id
        )

        app.logger.info(
            f"[BACK][routes/health_document.py][get_document_entries_route] "
            f"{len(entries)} documents récupérés pour user {user_id}, pro {health_professional_id}"
        )

        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(
            f"[BACK][routes/health_document.py][get_document_entries_route] "
            f"Erreur inattendue : {e}"
        )
        return jsonify({"error": str(e)}), 500


@document_bp.route('/<document_id>', methods=['PUT'])
@jwt_required()
def update_document_entry_route(health_professional_id, document_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()

        update_data = health_document_service.update_document_entry(
            user_id,
            document_id,
            new_data
        )

        if not update_data:
            return jsonify({"message": "Document introuvable."}), 404

        app.logger.info(
            f"[BACK][routes/health_document.py][update_document_entry_route] "
            f"Document {document_id} mis à jour pour user {user_id}"
        )

        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(
            f"[BACK][routes/health_document.py][update_document_entry_route] "
            f"Erreur inattendue : {e}"
        )
        return jsonify({"error": str(e)}), 500


@document_bp.route('/<document_id>', methods=['DELETE'])
@jwt_required()
def delete_document_entry_route(health_professional_id, document_id):
    try:
        user_id = get_jwt_identity()

        result = health_document_service.delete_document_entry(
            user_id,
            document_id
        )

        if not result:
            return jsonify({"message": "Document introuvable."}), 404

        app.logger.info(
            f"[BACK][routes/health_document.py][delete_document_entry_route] "
            f"Document {document_id} supprimé pour user {user_id}"
        )

        return jsonify(result), 200

    except Exception as e:
        app.logger.error(
            f"[BACK][routes/health_document.py][delete_document_entry_route] "
            f"Erreur inattendue : {e}"
        )
        return jsonify({"error": str(e)}), 500
