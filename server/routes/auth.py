from flask import Blueprint, request, jsonify
from model import db, User
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt
import os

auth_bp = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

def validate_password(password):
    """Validate password strength"""
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
        return jsonify({'error': 'Missing required fields'}), 400
        
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
        
    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 8 characters and contain uppercase, lowercase, and numbers'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate JWT token
    token = jwt.encode(
        {'user_id': user.id, 'username': user.username},
        os.environ.get('JWT_SECRET_KEY'),
        algorithm='HS256'
    )

    return jsonify({
        'message': 'Login successful',
        'token': token
    }), 200
