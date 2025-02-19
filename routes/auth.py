from flask import Blueprint, request, jsonify, session

auth = Blueprint('auth', __name__)

# Dummy user database
users = {
    "test@example.com": {
        "password": "password123",
        "name": "Test User"
    }
}

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if email in users and users[email]['password'] == password:
        session['user'] = users[email]['name']
        return jsonify({"message": "Login successful", "user": users[email]['name']}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"}), 200

@auth.route('/status', methods=['GET'])
def status():
    user = session.get('user')
    if user:
        return jsonify({"logged_in": True, "user": user}), 200
    return jsonify({"logged_in": False}), 200
