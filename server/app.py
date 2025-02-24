from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # <-- Import Migrate
from flask_jwt_extended import JWTManager
from database import db
from routes.auth import auth_bp
import routes
print("Routes module imported successfully!")

from routes import api_blueprint
print("api_blueprint imported successfully!")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # <-- Initialize Flask-Migrate
jwt = JWTManager(app)
limiter.init_app(app)

app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
