from  flask import current_app as app, request
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.services import auth_service

data_bp = Blueprint('data', __name__, url_prefix='/data')

# ------------------------------------------------------- Routes glycemia
@data_bp.route('/glycemia', methods=['POST'])
@jwt_required()
def glycemia():
    data = request.get_json()
    pass

# ------------------------------------------------------- Routes glycemia
@data_bp.route('/weight', methods=['POST'])
@jwt_required()
def weight():
    data = request.get_json()
    pass
