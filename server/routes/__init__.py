from flask import Blueprint
from .donations import donation_bp

api_blueprint = Blueprint("api", __name__)

# Import all route files to register endpoints
from .auth import auth_bp
from .donations import donation_bp  # Example additional route

# Register blueprints
api_blueprint.register_blueprint(auth_bp, url_prefix='/auth')
api_blueprint.register_blueprint(donation_bp, url_prefix='/donations')
