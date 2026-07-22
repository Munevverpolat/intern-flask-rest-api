import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # REST API endpointleri
    from app.routes import main

    app.register_blueprint(main)

    # Web UI sayfaları
    from app.web_routes import web

    app.register_blueprint(web)

    # =========================
    # LOGGING SETUP
    # =========================

    project_root = os.path.abspath(
        os.path.join(app.root_path, os.pardir)
    )

    logs_directory = os.path.join(project_root, "logs")

    os.makedirs(logs_directory, exist_ok=True)

    log_file = os.path.join(logs_directory, "app.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10240,
        backupCount=10,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s | %(name)s"
    )

    file_handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)

    if not any(
        isinstance(handler, RotatingFileHandler)
        for handler in app.logger.handlers
    ):
        app.logger.addHandler(file_handler)

    app.logger.info("Flask application started")

    # =========================
    # REQUEST LOGGING
    # =========================

    @app.before_request
    def log_request():
        app.logger.info(
            "[REQUEST] %s | %s %s",
            request.remote_addr,
            request.method,
            request.path,
        )

    # =========================
    # RESPONSE LOGGING
    # =========================

    @app.after_request
    def log_response(response):
        app.logger.info(
            "[RESPONSE] %s | STATUS=%s",
            request.path,
            response.status_code,
        )

        return response

    # =========================
    # ERROR LOGGING
    # =========================

    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(
            "[HTTP ERROR] 404 Endpoint not found: %s",
            request.path,
        )

        return {"error": "Endpoint not found"}, 404

    @app.errorhandler(Exception)
    def handle_error(error):
        if isinstance(error, HTTPException):
            app.logger.warning(
                "[HTTP ERROR] %s %s",
                error.code,
                error.description,
            )

            return {"error": error.description}, error.code

        app.logger.exception(
            "[ERROR] Unhandled exception: %s",
            str(error),
        )

        return {"error": "Internal Server Error"}, 500

    return app