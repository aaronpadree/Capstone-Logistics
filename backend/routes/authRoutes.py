from flask import Blueprint, request, session, make_response, jsonify
from services.authServices import create_user, login_user, google_login, google_callback

auth_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Route to create a new user
@auth_bp.route('/create', methods=['POST'])
def create_new_user():
    data = request.json 
    return create_user(data) 

# Log In Route
@auth_bp.route('/login', methods=['POST'])
def log_in_user():
    data = request.json
    return login_user(data)

@auth_bp.route('/google-login')
def google_login_route():
    return google_login()

@auth_bp.route('/google-callback')
def google_callback_route():
    return google_callback()

@auth_bp.route('/logout', methods=['POST'])
def log_out_user():
    session.clear()
    return make_response(jsonify({'message': 'Logged out successfully'}), 200)