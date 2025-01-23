from app import app
from flask import Blueprint, request
from services.authServices import create_user

auth_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Route to create a new department
@auth_bp.route('/create', methods=['POST'])
def create_new_user():
    data = request.json 
    return create_user(data) 
