from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    name = data.get('username')
    address = data.get('address')

    # Find the user by ID
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found", "status": "failure"}), 404

    # Update the allowed fields (Name and Address)
    if name:
        user.username = name
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
