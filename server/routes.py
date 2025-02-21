from flask import Blueprint, request, jsonify
from models import User, db

# Define the Blueprint
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing fields"}), 400
    
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
