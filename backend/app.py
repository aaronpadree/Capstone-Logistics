from flask import Flask, send_from_directory, abort, jsonify, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set a secret key for secure sessions
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
# Configure session type
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions in the filesystem
Session(app)  # Initialize session management

# Get the database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file or Render environment variables.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    redirect_uri='https://capstone-logistics.onrender.com/api/users/google-callback',
    client_kwargs={'scope': 'openid profile email'},
)

frontend_folder = os.path.join(os.getcwd(), "..", "frontend", "dist")

# Serve static files from the "dist" folder under the "frontend" directory
@app.route("/", defaults={"filename": ""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    try:
        return send_from_directory(frontend_folder, filename)
    except FileNotFoundError:
        abort(404)  # Return a 404 error if the file is not found

# Import the Blueprints
from routes.departmentRoutes import department_bp
from routes.supplierRoutes import supplier_bp
from routes.productsRoutes import product_bp
from routes.authRoutes import auth_bp
from routes.purchaseRoutes import purchase_bp
from routes.evaluateRoutes import evaluate_bp
from routes.damageRoutes import damage_bp
from routes.inventoryRoutes import inventory_bp
from routes.productsupplierRoutes import product_supplier_bp
from routes.maintenanceRoutes import maintenance_bp
from routes.departmentrequestRoutes import departmentrequest_bp

# Register the Blueprints
app.register_blueprint(department_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(evaluate_bp)
app.register_blueprint(damage_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(product_supplier_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(departmentrequest_bp)

# Test database connection
@app.route("/test-db")
def test_db():
    try:
        # Attempt to query the database
        result = db.session.execute("SELECT 1")
        return jsonify({"message": "Database connection successful", "result": [row[0] for row in result]})
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500

# Create the database tables
with app.app_context():
    db.create_all()

# Email and password login route
@app.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'success': True, 'user': {'email': user.email}})

@app.route('/signup', methods=['POST'])
def signup_post():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'success': False, 'message': 'Email address already exists'}), 400

    new_user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify({'success': True})

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)