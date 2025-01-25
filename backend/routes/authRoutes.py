from app import app
from flask import Blueprint, request, session
from services.authServices import create_user, login_user

auth_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Route to create a new department
@auth_bp.route('/create', methods=['POST'])
def create_new_user():
    data = request.json 
    return create_user(data) 

# Log In Route
@auth_bp.route('/login', methods=['POST'])
def log_in_user():
    data = request.json
    return login_user(data)

@auth_bp.route('/logout', methods=['POST'])
def log_out_user():
    session.clear()
    return make_response(jsonify({'message': 'Logged out successfully'}), 200)
