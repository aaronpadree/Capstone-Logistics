from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app import db, bcrypt
from models.users import User  # Correct import path

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Create new user
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify({'success': True, 'message': 'User registered successfully'})

# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'success': True, 'message': 'Login successful', 'user': {'email': user.email}})

# Logout
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Logout successful'})