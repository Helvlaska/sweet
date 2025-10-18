from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import meal_service

meal_bp = Blueprint('meal', __name__, url_prefix='/data/meal')
