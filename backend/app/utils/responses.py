from flask import jsonify

# ------------------------------ Fonction pour standardiser les succes messages
def success_response(part, file=None, element=None, message="", data=None, status_code=200):
    """
    Crée une réponse JSON uniforme pour un succès.
    """
    response = {
        "status": "success",
        "part": part,
        "file": file or "N/A",
        "element": element or "N/A",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

# ------------------------------- Fonction pour standardiser les error messages
def error_response(part, file=None, element=None, message="", data=None, status_code=400):
    """
    Crée une réponse JSON uniforme pour une erreur.
    """
    response = {
        "status": "error",
        "part": part,
        "file": file or "N/A",
        "element": element or "N/A",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code
