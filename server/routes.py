from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from models import db, User

@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = user.generate_token()
    return jsonify({'access_token': token, 'message': 'Login successful'}), 200

@api_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'You have access to this protected route'}), 200
@api_blueprint.route('/donate', methods=['POST'])
@jwt_required()
def donate():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    transaction_id = data.get('transaction_id')

    if not user_id or not amount or not transaction_id:
        return jsonify({'error': 'Missing required fields'}), 400

    donation = Donation(user_id=user_id, amount=amount)
    db.session.add(donation)
    db.session.commit()

    return jsonify({'message': 'Donation successful', 'transaction_id': transaction_id}), 201
