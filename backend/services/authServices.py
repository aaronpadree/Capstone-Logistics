import bcrypt
from flask import make_response, jsonify, session, redirect, url_for, request
from app import db
from models.users import User, RoleEnum
import requests
import os

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

def create_user(data):
    try:
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'staff') 

        existing_user_by_username = User.query.filter_by(username=username).first()
        if existing_user_by_username:
            return make_response(jsonify({'error': 'Username already exists'}), 400)

        existing_user_by_email = User.query.filter_by(email=email).first()
        if existing_user_by_email:
            return make_response(jsonify({'error': 'Email already exists'}), 400)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            username=username,
            password_hash=hashed_password.decode('utf-8'),
            email=email,
            role=RoleEnum[role.upper()] if role.upper() in RoleEnum.__members__ else RoleEnum.STAFF
        )

        db.session.add(new_user)
        db.session.commit()

        user_response = {
            'user_id': new_user.user_id,
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.role.value,
            'created_at': new_user.created_at,
            'updated_at': new_user.updated_at
        }

        return make_response(jsonify({'message': 'User created successfully', 'user': user_response}), 201)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

def login_user(data):
    try:
        username = data.get('username')
        password = data.get('password')

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response(jsonify({'error': 'Invalid username or password'}), 401)

        # Verify the password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return make_response(jsonify({'error': 'Invalid username or password'}), 401)

        # Store user information in session
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['role'] = user.role.value

        return make_response(jsonify({
            'message': 'Login successful',
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value
            }
        }), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def google_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = requests.Request(
        'GET',
        authorization_endpoint,
        params={
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": url_for("users.google_callback_route", _external=True),
            "scope": "openid email profile",
            "response_type": "code",
            "state": "random_state_string"
        }
    ).prepare().url

    return redirect(request_uri)

def google_callback():
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = requests.Request(
        'POST',
        token_endpoint,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": request.args.get("code"),
            "redirect_uri": url_for("users.google_callback_route", _external=True),
            "grant_type": "authorization_code"
        }
    ).prepare().url

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    token_json = token_response.json()
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = requests.Request(
        'GET',
        userinfo_endpoint,
        headers={"Authorization": f"Bearer {token_json['access_token']}"}
    ).prepare().url

    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo = userinfo_response.json()

    if not userinfo.get("email_verified"):
        return "User email not available or not verified by Google.", 400

    unique_id = userinfo["sub"]
    users_email = userinfo["email"]
    users_name = userinfo["given_name"]

    user = User.query.filter_by(email=users_email).first()
    if not user:
        user = User(
            username=users_name,
            email=users_email,
            password_hash="",
            role=RoleEnum.STAFF
        )
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.user_id
    session['username'] = user.username
    session['role'] = user.role.value

    return redirect(url_for("index"))