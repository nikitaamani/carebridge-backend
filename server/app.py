from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # <-- Import Migrate
from flask_jwt_extended import JWTManager
from database import db
from routes import api_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # <-- Initialize Flask-Migrate
jwt = JWTManager(app)

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
