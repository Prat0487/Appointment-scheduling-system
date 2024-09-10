"""
  This module provides user authentication and session management functionality for a Flask web application.
  
  The module includes the following features:
  - User registration: Allows users to register with a username and password. Passwords are hashed using bcrypt.
  - User authentication: Allows users to log in with their username and password. Passwords are checked against the hashed values stored in the mock database.
  - Session management: Provides session-based authentication, where a user's login status is stored in the session. Sessions are set to be permanent and have a lifetime of 30 minutes.
  - Protected routes: Provides a decorator `login_required` that can be used to protect routes, requiring the user to be logged in to access them.
  
  The module uses a mock database (a Python dictionary) to store user information. In a production environment, this would be replaced with a real database.
"""
import bcrypt
from flask import Flask, request, session, jsonify
from functools import wraps
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key
app.permanent_session_lifetime = timedelta(minutes=30)  # Set session lifetime to 30 minutes

# Mock database for users (replace with actual database in production)
users = {}

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def register_user(username, password):
    if username in users:
        return False, 'Username already exists'
    
    hashed_password = hash_password(password)
    users[username] = hashed_password
    return True, 'User registered successfully'

def authenticate_user(username, password):
    if username not in users:
        return False
    return check_password(password, users[username])

@app.before_request
def make_session_permanent():
    session.permanent = True  # Make the session permanent

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    success, message = register_user(username, password)
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'error': message}), 400

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if authenticate_user(username, password):
        session['username'] = username
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'}), 200

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': 'This is a protected route', 'user': session['username']}), 200

if __name__ == '__main__':
    app.run(debug=True)
