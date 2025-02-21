# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from routes import api_blueprint

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Register blueprints
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures tables are created
    app.run(debug=True)
