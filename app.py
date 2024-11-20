# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Welcome to Team 3'

# if __name__ == '__main__':
#     app.run()

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

# Create the database tables (run once)
with app.app_context():
    db.create_all()

# You can add real users manually or via an API
# For example, you can insert users into the database using the following:
# user1 = User(email='user1@bolton.ac.uk', password=generate_password_hash('password123'), username='user1')
# db.session.add(user1)
# db.session.commit()

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
                    "email": user.email
                }
            }), 200
        else:
            return jsonify({"message": "Incorrect password", "status": "failure"}), 401
    else:
        return jsonify({"message": "User not found", "status": "failure"}), 404


if __name__ == '__main__':
    app.run(debug=True)

