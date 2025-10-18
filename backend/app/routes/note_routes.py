from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services import note_service

note_bp = Blueprint('note', __name__, url_prefix='/data/note')
