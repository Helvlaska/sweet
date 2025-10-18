from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import professional_service

professional_bp = Blueprint('professional', __name__, url_prefix='/data/professional')
