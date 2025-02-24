from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from server.models import db, User
import re
from flask_limiter import Limiter
limiter = Limiter(key_func=get_remote_address)
from flask_limiter.util import get_remote_address
import jwt
import os
import datetime


auth_bp = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

def validate_password(password):
    """Ensure password is strong (min 8 chars, 1 uppercase, 1 lowercase, 1 number)"""
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
        
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
        
    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 8 characters and include uppercase, lowercase, and a number'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'A user with this email or username already exists'}), 400

    try:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Account successfully created!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed, please try again'}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting to prevent brute-force attacks
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Ensure JWT Secret Key is set
    secret_key = os.environ.get('JWT_SECRET_KEY')
    if not secret_key:
        return jsonify({'error': 'Server misconfiguration: Missing JWT_SECRET_KEY'}), 500

    # Generate JWT token with expiration
    token = jwt.encode(
        {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
        },
        secret_key,
        algorithm='HS256'
    )

    return jsonify({
        'message': 'Login successful',
        'token': token
    }), 200
