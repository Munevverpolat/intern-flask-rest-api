from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "super-secret-key"

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://flask_user:StrongPassword123@localhost/intern_flask_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import main
    from app.models import User
    app.register_blueprint(main)

    return app
