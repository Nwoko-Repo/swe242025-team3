from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to Team 3'

if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify

app = Flask(__name__)

users_db = {
    'user1': {'password': 'password123', 'email': 'user1@example.com'},
    'user2': {'password': 'securepass456', 'email': 'user2@example.com'}
}

# Login API
@app.route('/login', methods=['POST'])
def login():
    # Get the data from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Perform a check to see if username exists in the database
    if username in users_db:
        user = users_db[username]
        # Validate the password and email
        if user['password'] == password and user['email'] == email:
            return jsonify({"message": "Login successful", "status": "success"}), 200
        else:
            return jsonify({"message": "Incorrect username, password, or email", "status": "failure"}), 401
    else:
        return jsonify({"message": "User not found", "status": "failure"}), 404

if __name__ == '__main__':
    app.run(debug=True)
