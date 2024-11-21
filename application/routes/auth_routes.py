from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import Administrator, Customer, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from application.utils import ResponseHelper  # Import the helper class
import json  # Import JSON for serialization and deserialization

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register Endpoint
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'customer')  # Default role: customer

    # Validate input
    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if user already exists
    if Customer.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    if Customer.query.filter_by(name=username).first():
        return jsonify({"message": "Username already taken"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user (Customer role)
    if role == "customer":
        user = Customer(
            customerID=f"cust-{datetime.datetime.utcnow().timestamp()}",
            name=username,
            email=email,
            password=hashed_password
        )
    # Create an administrator
    elif role == "administrator":
        user = Administrator(
            adminID=f"admin-{datetime.datetime.utcnow().timestamp()}",
            name=username,
            email=email,
            permissions="full_access",
            password=hashed_password
        )
    else:
        return jsonify({"message": "Invalid role"}), 400

    # Save the user
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login Endpoint
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find user
    user = Customer.query.filter_by(email=email).first() or Administrator.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return ResponseHelper.default_response("Invalid credentials", 401)

    # Create token
    role = "customer" if isinstance(user, Customer) else "administrator"
    identity = json.dumps({"id": user.customerID if role == "customer" else user.adminID, "role": role})
    access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(hours=1))

    data = {
        "access_token": access_token,
        "role": role
    }
    return ResponseHelper.default_response("Login successful", 200, data)



@auth_bp.route('/user-details', methods=['GET'])
@jwt_required()
def get_user_details():
    """
    Protected endpoint to fetch authenticated user details.
    """
    # Get the current user identity from the JWT
    current_user = json.loads(get_jwt_identity())  # Deserialize the identity

    # Check the role and retrieve user details from the database
    if current_user['role'] == 'customer':
        user = Customer.query.filter_by(customerID=current_user['id']).first()
    elif current_user['role'] == 'administrator':
        user = Administrator.query.filter_by(adminID=current_user['id']).first()
    else:
        return ResponseHelper.default_response("Invalid role", 403)

    if not user:
        return ResponseHelper.default_response("User not found", 404)

    # Build the response data
    user_data = {
        "id": user.customerID if current_user['role'] == 'customer' else user.adminID,
        "name": user.name,
        "email": user.email,
        "role": current_user['role']
    }

    return ResponseHelper.default_response("User details fetched successfully", 200, user_data)


