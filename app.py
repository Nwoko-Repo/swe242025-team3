from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load .env variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite for simplicity

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Authentication API"}
)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

# Register blueprints
from application.routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")
from application.routes.product_routes import product_bp
app.register_blueprint(product_bp)
from application.routes.institution_routes import institution_bp
app.register_blueprint(institution_bp)
from application.routes.iot_device_routes import iot_device_bp
app.register_blueprint(iot_device_bp)
from application.routes.api_access_routes import api_access_bp
app.register_blueprint(api_access_bp)


# Ensure database tables are created
first_request = True

@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    return {"message": "Welcome to Flask Authentication API"}

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {e}")


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=True)  # Added Address field

# Create the database tables (run once)
with app.app_context():
    db.create_all()

# Login API
@app.route('/login', methods=['POST'])
def login():
    # Get the data from the request
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the email exists in the database
    user = User.query.filter_by(email=email).first()

    if user:
        # Check if the password is correct
        if check_password_hash(user.password, password):
            # Return user information (excluding the password)
            return jsonify({
                "message": "Login successful",
                "status": "success",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "address": user.address
                }
            }), 200
        else:
            return jsonify({"message": "Incorrect password", "status": "failure"}), 401
    else:
        return jsonify({"message": "User not found", "status": "failure"}), 404

# Amend User Details API
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    email = data.get('email')
    address = data.get('address')

    # Find the user by ID
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found", "status": "failure"}), 404

    # Update the allowed fields (Name and Address)
    if email:
        user.email = email
    if address:
        user.address = address

    # Save changes to the database
    db.session.commit()

    return jsonify({
        "message": "User details updated successfully",
        "status": "success",
        "user": {
            "username": user.username,
            "email": user.email,
            "address": user.address
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
