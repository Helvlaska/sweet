"""
[BACK][routes/health_document_routes.py]

Blueprint : document_bp — prefix /data/health_professionals/<health_professional_id>/documents
Authentication : JWT required on all routes (@jwt_required)

Exposed routes:
  POST   /                  Upload one or more documents for a health professional
  GET    /                  Retrieve all documents for a health professional
  PUT    /<document_id>     Update a document (filename or file)
  DELETE /<document_id>     Delete a document

HTTP status codes:
  201  Resource created
  200  Success (read / update)
  204  Success (delete, no content)
  400  Missing or malformed data
  401  Missing or invalid token
  404  Resource not found
  422  Data present but invalid (limit reached, wrong type or format)
  500  Unexpected server error
"""


from flask import current_app as app, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import health_document_service


document_bp = Blueprint('document', __name__, url_prefix='/data/health_professionals/<health_professional_id>/documents')


@document_bp.route('/', methods=['POST'])
@jwt_required()
def create_document_entry_route(health_professional_id):
    """Upload one or more documents for a health professional."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)

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

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/health_document_routes.py][create_document_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/health_document.py][create_document_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@document_bp.route('/', methods=['GET'])
@jwt_required()
def get_document_entries_route(health_professional_id):
    """Retrieve all documents for a given health professional."""
    try:
        user_id = get_jwt_identity()
        entries = health_document_service.get_documents_by_pro(user_id, health_professional_id)
        app.logger.info(
            f"[BACK][routes/health_document.py][get_document_entries_route]"
            f"{len(entries)} documents récupérés pour user {user_id}, pro {health_professional_id}"
        )
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/health_document_routes.py][get_document_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@document_bp.route('/<document_id>', methods=['PUT'])
@jwt_required()
def update_document_entry_route(health_professional_id, document_id):
    """Update a document filename or file content."""
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({"error": "Missing request body"}), 400

        update_data = health_document_service.update_document_entry(user_id, document_id, new_data)
        if not update_data:
            return jsonify({"message": "Document introuvable."}), 404

        app.logger.info(
            f"[BACK][routes/health_document.py][update_document_entry_route] "
            f"Document {document_id} mis à jour pour user {user_id}"
        )
        return jsonify(update_data), 200

    except (ValueError, TypeError) as e:
        app.logger.error(f"[BACK][routes/health_document_routes.py][update_document_entry_route] Données invalides : {e}")
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error(f"[BACK][routes/health_document_routes.py][update_document_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500


@document_bp.route('/<document_id>', methods=['DELETE'])
@jwt_required()
def delete_document_entry_route(health_professional_id, document_id):
    """Delete a document."""
    try:
        user_id = get_jwt_identity()
        result = health_document_service.delete_document_entry(user_id, document_id)
        if not result:
            return jsonify({"message": "Document introuvable."}), 404

        app.logger.info(
            f"[BACK][routes/health_document.py][delete_document_entry_route] "
            f"Document {document_id} supprimé pour user {user_id}"
        )
        return jsonify(result), 204

    except Exception as e:
        app.logger.error(f"[BACK][routes/health_document_routes.py][delete_document_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": "Internal server error"}), 500
