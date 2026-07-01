from flask import Flask, request
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main
    app.register_blueprint(main)

    # =========================
    # LOGGING SETUP
    # =========================
    if not app.debug:

        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240,
            backupCount=10
        )

        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s | %(name)s'
        )

        file_handler.setFormatter(formatter)

        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.info('Flask application started')

    # =========================
    # REQUEST LOGGING (EVERY REQUEST)
    # =========================
    @app.before_request
    def log_request():
        app.logger.info(
            f"[REQUEST] {request.remote_addr} | {request.method} {request.path}"
        )

    # =========================
    # RESPONSE LOGGING (EVERY RESPONSE)
    # =========================
    @app.after_request
    def log_response(response):
        app.logger.info(
            f"[RESPONSE] {request.path} | STATUS={response.status_code}"
        )
        return response

    # =========================
    # ERROR LOGGING (GLOBAL)
    # =========================

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Endpoint not found"}, 404

    @app.errorhandler(Exception)
    def handle_error(e):

        if isinstance(e, HTTPException):
            app.logger.warning(f"[HTTP ERROR] {e.code} {e.description}")
            return {"error": e.description}, e.code

        app.logger.error(f"[ERROR] {str(e)}")
        return {"error": "Internal Server Error"}, 500
    
    return app