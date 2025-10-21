from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import medication_service

medication_bp = Blueprint('medication', __name__, url_prefix='/data/medication')


@medication_bp.route('/', methods=['POST'])
@jwt_required()
def create_medication_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = medication_service.create_medication_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_medication_entry_route] Nouveau médicament '{new_entry.get('name')}' ajouté pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_medication_entry_route] Erreur inattendue lors de la création d’un médicament : {e}")
        return jsonify({"error": str(e)}), 500


@medication_bp.route('/', methods=['GET'])
@jwt_required()
def get_medication_entry_route():
    try:
        user_id = get_jwt_identity()
        entries = medication_service.get_medication_entry(user_id)
        app.logger.info(f"[BACK][routes/data.py][get_medication_entry_route] {len(entries)} médicaments récupérés pour user {user_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_medication_entry_route] Erreur inattendue lors de la récupération des médicaments : {e}")
        return jsonify({"error": str(e)}), 500


@medication_bp.route('/<entry_id>', methods=['PUT'])
@jwt_required()
def update_medication_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        updated_entry = medication_service.update_medication_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_medication_entry_route] Médicament {entry_id} mis à jour pour user {user_id}")
        return jsonify(updated_entry), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_medication_entry_route] Erreur inattendue lors de la mise à jour : {e}")
        return jsonify({"error": str(e)}), 500


@medication_bp.route('/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_medication_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = medication_service.delete_medication_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_medication_entry_route] Médicament {entry_id} supprimé pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_medication_entry_route] Erreur inattendue lors de la suppression : {e}")
        return jsonify({"error": str(e)}), 500


@medication_bp.route('/<entry_id>/take', methods=['PATCH'])
@jwt_required()
def take_medication_dose_route(entry_id):
    """Décrémente le stock du médicament correspondant"""
    try:
        user_id = get_jwt_identity()
        updated_entry = medication_service.take_medication_dose(user_id, entry_id)
        if not updated_entry:
            app.logger.error("[BACK][routes/data.py][take_medication_dose_route] Médicament introuvable")
            return jsonify({"error": "Médicament introuvable"}), 404
        app.logger.info(f"[BACK][routes/data.py][take_medication_dose_route] Prise enregistrée pour user {user_id} sur médicament {entry_id}")
        return jsonify(updated_entry), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][take_medication_dose_route] Erreur inattendue lors de l’enregistrement de la prise : {e}")
        return jsonify({"error": str(e)}), 500
