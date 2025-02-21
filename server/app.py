# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app import db 
from routes import api_blueprint

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
db.init_app(app)
from models import User 

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
