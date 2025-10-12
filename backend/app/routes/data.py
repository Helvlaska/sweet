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
        app.logger.info(f"[BACK][routes/data.py][create_activity_entry_route] Nouvelle entrée créée pour user {user_id}")
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


# ------------------------------------------------------- Routes HealthProfessional
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
