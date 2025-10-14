from  flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import data_service

data_bp = Blueprint('data', __name__, url_prefix='/data')

# ------------------------------------------------------- Routes glycemia
@data_bp.route('/glycemia', methods=['POST'])
@jwt_required()
def create_glycemia_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_glycemia_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_glycemia_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_glycemia_entry_route()] Erreur inattendue pour l'entré d'une nouvelle mesure : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/glycemia', methods=['GET'])
@jwt_required()
def get_glycemia_entries_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_glycemia_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_entries_route()] {len(entries)} mesures récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_glycemia_entries_route()] Erreur inattendue pour la récupération des mesures : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/glycemia/stats', methods=['GET'])
@jwt_required()
def get_glycemia_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = data_service.get_glycemia_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_glycemia_stats_route()] Moyenne glycémique récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_glycemia_stats_route()] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/glycemia/<entry_id>', methods=['PUT'])
@jwt_required()
def update_glycemia_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_glycemia_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_glycemia_entry_route()] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_glycemia_entry_route()] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/glycemia/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_glycemia_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_glycemia_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_glycemia_entry_route()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_glycemia_entry_route()] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------- Routes weight
@data_bp.route('/weight', methods=['POST'])
@jwt_required()
def create_weight_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_weight_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_weight_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_weight_entry_route()] Erreur inattendue pour l'entré d'une nouvelle mesure : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/weight', methods=['GET'])
@jwt_required()
def get_weight_entries_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_weight_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_weight_entries_route()] {len(entries)} mesures récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_weight_entries_route()] Erreur inattendue pour la récupération des mesures : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/weight/stats', methods=['GET'])
@jwt_required()
def get_weight_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = data_service.get_weight_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_weight_stats_route()] Moyenne de poids récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_weight_stats_route()] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/weight/<entry_id>', methods=['PUT'])
@jwt_required()
def update_weight_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_weight_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_weight_entry_route()] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_weight_entry_route()] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/weight/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_weight_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_weight_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_weight_entry_route()] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_weight_entry_route()] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------- Routes activity
@data_bp.route('/activity', methods=['POST'])
@jwt_required()
def create_activity_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_activity_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_activity_entry_route] Nouvelle entrée {new_entry} créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_activity_entry_route] Erreur inattendue pour l'entré d'une nouvelle activité : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_activity_entry_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_activity_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_activity_entry_route()] {len(entries)} activités récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_activity_entry_route()] Erreur inattendue pour la récupération des activités : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/activity/stats', methods=['GET'])
@jwt_required()
def get_activity_stats_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        result = data_service.get_activity_stats(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_activity_stats_route] Moyenne de temps d'activité récupérée pour user {user_id}, période '{range_type}', date '{target_date}'")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_activity_stats_route] Erreur inattendue pour la récupération des stats : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/activity/<entry_id>', methods=['PUT'])
@jwt_required()
def update_activity_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_activity_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_activity_entry_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_activity_entry_route] Erreur inattendue pour la modification de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/activity/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_activity_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_activity_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_activity_entry_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_activity_entry_route] Erreur inattendue lors de la suppression de la valeur : {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------- Routes meal
@data_bp.route('/meal', methods=['POST'])
@jwt_required()
def create_meal_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_meal_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_meal_entry_route] Nouvelle entrée créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_meal_entry_route] Erreur inattendue pour l'entré d'un nouveau repas : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/meal', methods=['GET'])
@jwt_required()
def get_meal_entry_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_meal_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_meal_entry_route()] {len(entries)} repas récupérées pour user {user_id}, période {range_type}, date {target_date}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_meal_entry_route()] Erreur inattendue pour la récupération des repas : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/meal/<entry_id>', methods=['PUT'])
@jwt_required()
def update_meal_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_meal_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_meal_entry_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_meal_entry_route] Erreur inattendue pour la modification du repas : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/meal/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_meal_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_meal_entry_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_meal_entry_route] Erreur inattendue lors de la suppression du repas : {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------- Routes mood
@data_bp.route('/mood', methods=['POST'])
@jwt_required()
def create_mood_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_mood_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_mood_entry_route] Nouvelle humeur '{new_entry.get('description')}' créée pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_mood_entry_route] Erreur inattendue lors de la création d'une nouvelle humeur : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/mood', methods=['GET'])
@jwt_required()
def get_mood_entry_route():
    try:
        user_id = get_jwt_identity()
        range_type = request.args.get("range_type", "day")
        target_date = request.args.get("target_date", None)
        entries = data_service.get_mood_entry(user_id, range_type, target_date)
        app.logger.info(f"[BACK][routes/data.py][get_mood_entry_route] {len(entries)} humeurs récupérées pour user {user_id}, période {range_type}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_mood_entry_route] Erreur inattendue lors de la récupération des humeurs : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/mood/<entry_id>', methods=['PUT'])
@jwt_required()
def update_mood_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_mood_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_mood_entry_route] Humeur {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_mood_entry_route] Erreur inattendue lors de la mise à jour de l’humeur : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/mood/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_mood_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_mood_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_mood_entry_route] Humeur {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_mood_entry_route] Erreur inattendue lors de la suppression de l’humeur : {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------- Routes medication
@data_bp.route('/medication', methods=['POST'])
@jwt_required()
def create_medication_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_medication_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_medication_entry_route] Nouveau médicament '{new_entry.get('name')}' ajouté pour user {user_id}")
        return jsonify(new_entry), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_medication_entry_route] Erreur inattendue lors de la création d’un médicament : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/medication', methods=['GET'])
@jwt_required()
def get_medication_entry_route():
    try:
        user_id = get_jwt_identity()
        entries = data_service.get_medication_entry(user_id)
        app.logger.info(f"[BACK][routes/data.py][get_medication_entry_route] {len(entries)} médicaments récupérés pour user {user_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_medication_entry_route] Erreur inattendue lors de la récupération des médicaments : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/medication/<entry_id>', methods=['PUT'])
@jwt_required()
def update_medication_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        updated_entry = data_service.update_medication_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_medication_entry_route] Médicament {entry_id} mis à jour pour user {user_id}")
        return jsonify(updated_entry), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_medication_entry_route] Erreur inattendue lors de la mise à jour : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/medication/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_medication_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_medication_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_medication_entry_route] Médicament {entry_id} supprimé pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_medication_entry_route] Erreur inattendue lors de la suppression : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/medication/take/<entry_id>', methods=['PATCH'])
@jwt_required()
def take_medication_dose_route(entry_id):
    """Décrémente le stock du médicament correspondant"""
    try:
        user_id = get_jwt_identity()
        updated_entry = data_service.take_medication_dose(user_id, entry_id)
        if not updated_entry:
            app.logger.error("[BACK][routes/data.py][take_medication_dose_route] Médicament introuvable")
            return jsonify({"error": "Médicament introuvable"}), 404
        app.logger.info(f"[BACK][routes/data.py][take_medication_dose_route] Prise enregistrée pour user {user_id} sur médicament {entry_id}")
        return jsonify(updated_entry), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][take_medication_dose_route] Erreur inattendue lors de l’enregistrement de la prise : {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------- Routes HealthProfessional
@data_bp.route('/healthprofessional', methods=['POST'])
@jwt_required()
def create_health_professional_entry_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_health_professional_entry(user_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_health_professional_entry_route] Nouveau professionnel créé pour user {user_id}")
        return jsonify(new_entry.to_dict()), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/healthprofessional', methods=['GET'])
@jwt_required()
def get_health_professional_entries_route():
    try:
        user_id = get_jwt_identity()
        entries = data_service.get_health_professional_entries(user_id)
        app.logger.info(f"[BACK][routes/data.py][get_health_professional_entries_route] {len(entries)} professionnels récupérés pour user {user_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_health_professional_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/healthprofessional/<professional_id>/notes', methods=['GET'])
@jwt_required()
def get_health_professional_with_notes_route(professional_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.get_health_professional_with_notes(user_id, professional_id)
        if not result:
            return jsonify({"message": "Aucun professionnel trouvé pour cet utilisateur."}), 404
        app.logger.info(f"[BACK][routes/data.py][get_health_professional_with_notes_route] Données pro+notes envoyées pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_health_professional_with_notes_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500



@data_bp.route('/healthprofessional/<entry_id>', methods=['PUT'])
@jwt_required()
def update_health_professional_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_health_professional_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_health_professional_entry_route] Entrée {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/healthprofessional/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_health_professional_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_health_professional_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_health_professional_entry_route] Entrée {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_health_professional_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------- Routes Notes
@data_bp.route('/note/<health_professional_id>', methods=['POST'])
@jwt_required()
def create_note_entry_route(health_professional_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_entry = data_service.create_note_entry(user_id, health_professional_id, data)
        app.logger.info(f"[BACK][routes/data.py][create_note_entry_route] Nouvelle note créée pour user {user_id}, pro {health_professional_id}")
        return jsonify(new_entry.to_dict()), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][create_note_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/note/<health_professional_id>', methods=['GET'])
@jwt_required()
def get_note_entries_route(health_professional_id):
    try:
        user_id = get_jwt_identity()
        entries = data_service.get_note_entries(user_id, health_professional_id)
        app.logger.info(f"[BACK][routes/data.py][get_note_entries_route] {len(entries)} notes récupérées pour user {user_id}, pro {health_professional_id}")
        return jsonify(entries), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][get_note_entries_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/note/<entry_id>', methods=['PUT'])
@jwt_required()
def update_note_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        new_data = request.get_json()
        update_data = data_service.update_note_entry(user_id, entry_id, new_data)
        app.logger.info(f"[BACK][routes/data.py][update_note_entry_route] Note {entry_id} mise à jour pour user {user_id}")
        return jsonify(update_data), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][update_note_entry_route] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route('/note/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_note_entry_route(entry_id):
    try:
        user_id = get_jwt_identity()
        result = data_service.delete_note_entry(entry_id, user_id)
        app.logger.info(f"[BACK][routes/data.py][delete_note_entry_route] Note {entry_id} supprimée avec succès pour user {user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][delete_note_entry_route] Erreur inattendue lors de la suppression : {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------ Routes ForumPost
@data_bp.route("/forum/posts", methods=["POST"])
@jwt_required()
def route_create_forum_post():
    """Crée un nouveau post de forum."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error("[BACK][routes/data.py][route_create_forum_post] Requête vide ou invalide")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        post = data_service.create_forum_post_entry(current_user_id, data)
        if not post:
            return jsonify({"error": "Création du post impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_create_forum_post] Post créé par user {current_user_id}")
        return jsonify(post.to_dict()), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_create_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/posts", methods=["GET"])
def route_get_all_forum_posts():
    """Récupère la liste complète des posts (tri date/popularité)."""
    try:
        sort_by = request.args.get("sort_by", "recent")
        posts = data_service.get_all_forum_posts(sort_by)
        if posts is None or len(posts) == 0:
            return jsonify({"message": "Aucun post trouvé"}), 200
        app.logger.info(f"[BACK][routes/data.py][route_get_all_forum_posts] {len(posts)} posts récupérés (sort_by={sort_by})")
        return jsonify(posts), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_all_forum_posts] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/posts/<string:post_id>", methods=["GET"])
def route_get_forum_post_by_id(post_id):
    """Récupère un post précis avec ses commentaires."""
    try:
        post = data_service.get_forum_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post introuvable"}), 404
        app.logger.info(f"[BACK][routes/data.py][route_get_forum_post_by_id] Post {post_id} récupéré")
        return jsonify(post), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_forum_post_by_id] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/posts/<string:post_id>", methods=["PUT"])
@jwt_required()
def route_update_forum_post(post_id):
    """Met à jour un post (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400
        updated_post = data_service.update_forum_post_entry(post_id, data, current_user_id)
        if not updated_post:
            return jsonify({"error": "Modification impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_update_forum_post] Post {post_id} mis à jour par user {current_user_id}")
        return jsonify(updated_post.to_dict()), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_update_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/posts/<string:post_id>", methods=["DELETE"])
@jwt_required()
def route_delete_forum_post(post_id):
    """Supprime un post (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        result = data_service.delete_forum_post(post_id, current_user_id)
        if not result:
            return jsonify({"error": "Suppression impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_delete_forum_post] Post {post_id} supprimé par user {current_user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_delete_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/posts/<string:post_id>/like", methods=["POST"])
@jwt_required()
def route_toggle_like_forum_post(post_id):
    """Ajoute ou retire un like sur un post."""
    try:
        current_user_id = get_jwt_identity()
        result = data_service.toggle_like_forum_post(post_id, current_user_id)
        if not result:
            return jsonify({"error": "Action impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_toggle_like_forum_post] User {current_user_id} → {result['message']} sur post {post_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_toggle_like_forum_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------- Routes Comment
@data_bp.route("/forum/posts/<string:post_id>/comments", methods=["POST"])
@jwt_required()
def route_create_comment(post_id):
    """Crée un commentaire associé à un post."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error("[BACK][routes/data.py][route_create_comment] Requête vide ou invalide")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        comment = data_service.create_comment_entry(post_id, current_user_id, data)
        if not comment:
            app.logger.error("[BACK][routes/data.py][route_create_comment] Échec de création du commentaire")
            return jsonify({"error": "Création du commentaire impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_create_comment] Commentaire créé sur post {post_id} par user {current_user_id}")
        return jsonify(comment.to_dict()), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_create_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/posts/<string:post_id>/comments", methods=["GET"])
def route_get_comments_by_post(post_id):
    """Récupère tous les commentaires d’un post donné."""
    try:
        comments = data_service.get_comments_by_post(post_id)
        if comments is None:
            app.logger.warning(f"[BACK][routes/data.py][route_get_comments_by_post] Aucun commentaire trouvé pour le post {post_id}")
            return jsonify({"message": "Aucun commentaire trouvé"}), 200
        for comment in comments:
            app.logger.debug(f"[BACK][routes/data.py][route_get_comments_by_post] Commentaire trouvé → {comment.get('id')}")
        app.logger.info(f"[BACK][routes/data.py][route_get_comments_by_post] {len(comments)} commentaires récupérés pour le post {post_id}")
        return jsonify(comments), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_comments_by_post] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/comments/<string:comment_id>", methods=["PUT"])
@jwt_required()
def route_update_comment(comment_id):
    """Met à jour un commentaire (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error("[BACK][routes/data.py][route_update_comment] Aucune donnée reçue pour la mise à jour")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        updated_comment = data_service.update_comment_entry(comment_id, current_user_id, data)
        if not updated_comment:
            app.logger.error(f"[BACK][routes/data.py][route_update_comment] Mise à jour du commentaire {comment_id} impossible")
            return jsonify({"error": "Mise à jour impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_update_comment] Commentaire {comment_id} mis à jour par user {current_user_id}")
        return jsonify(updated_comment), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_update_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/comments/<string:comment_id>", methods=["DELETE"])
@jwt_required()
def route_delete_comment(comment_id):
    """Supprime un commentaire (uniquement par son auteur)."""
    try:
        current_user_id = get_jwt_identity()
        result = data_service.delete_comment_entry(comment_id, current_user_id)
        if not result:
            app.logger.error(f"[BACK][routes/data.py][route_delete_comment] Suppression du commentaire {comment_id} impossible")
            return jsonify({"error": "Suppression impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_delete_comment] Commentaire {comment_id} supprimé par user {current_user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_delete_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/forum/comments/<string:comment_id>/like", methods=["POST"])
@jwt_required()
def route_toggle_like_comment(comment_id):
    """Ajoute ou retire un like sur un commentaire."""
    try:
        current_user_id = get_jwt_identity()
        result = data_service.toggle_like_comment(comment_id, current_user_id)
        if not result:
            app.logger.error(f"[BACK][routes/data.py][route_toggle_like_comment] Action impossible pour le commentaire {comment_id}")
            return jsonify({"error": "Action impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_toggle_like_comment] User {current_user_id} → {result['message']} sur commentaire {comment_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_toggle_like_comment] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------------------- Routes Article
@data_bp.route("/articles", methods=["POST"])
@jwt_required()
def route_create_article():
    """Crée un nouvel article (admin uniquement)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            app.logger.error("[BACK][routes/data.py][route_create_article] Aucune donnée reçue")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        article = data_service.create_article_entry(data, current_user_id)
        if not article:
            return jsonify({"error": "Création de l'article impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_create_article] Article créé par admin {current_user_id}")
        return jsonify(article.to_dict()), 201

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_create_article] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/articles", methods=["GET"])
def route_get_all_articles():
    """Récupère tous les articles (triés par date ou popularité)."""
    try:
        sort_by = request.args.get("sort_by", "recent")
        articles = data_service.get_all_articles(sort_by)
        if articles is None or len(articles) == 0:
            return jsonify({"message": "Aucun article trouvé"}), 200
        app.logger.info(f"[BACK][routes/data.py][route_get_all_articles] {len(articles)} articles récupérés (sort_by={sort_by})")
        return jsonify(articles), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_all_articles] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/articles/<string:article_id>", methods=["GET"])
def route_get_article_by_id(article_id):
    """Récupère un article précis."""
    try:
        article = data_service.get_article_by_id(article_id)
        if not article:
            return jsonify({"error": "Article introuvable"}), 404
        app.logger.info(f"[BACK][routes/data.py][route_get_article_by_id] Article {article_id} récupéré")
        return jsonify(article), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_get_article_by_id] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/articles/<string:article_id>", methods=["PUT"])
@jwt_required()
def route_update_article(article_id):
    """Met à jour un article (admin uniquement)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400
        updated_article = data_service.update_article_entry(article_id, current_user_id, data)
        if not updated_article:
            return jsonify({"error": "Mise à jour impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_update_article] Article {article_id} mis à jour par admin {current_user_id}")
        return jsonify(updated_article), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_update_article] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/articles/<string:article_id>", methods=["DELETE"])
@jwt_required()
def route_delete_article(article_id):
    """Supprime un article (admin uniquement)."""
    try:
        current_user_id = get_jwt_identity()
        result = data_service.delete_article_entry(article_id, current_user_id)
        if not result:
            return jsonify({"error": "Suppression impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_delete_article] Article {article_id} supprimé par admin {current_user_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_delete_article] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500


@data_bp.route("/articles/<string:article_id>/like", methods=["POST"])
@jwt_required()
def route_toggle_like_article(article_id):
    """Ajoute ou retire un like sur un article."""
    try:
        current_user_id = get_jwt_identity()
        result = data_service.toggle_like_article(article_id, current_user_id)
        if not result:
            return jsonify({"error": "Action impossible"}), 400
        app.logger.info(f"[BACK][routes/data.py][route_toggle_like_article] User {current_user_id} → {result['message']} sur article {article_id}")
        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"[BACK][routes/data.py][route_toggle_like_article] Erreur inattendue : {e}")
        return jsonify({"error": str(e)}), 500
