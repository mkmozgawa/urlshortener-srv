import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from src.api.urls import urls_bp
    app.register_blueprint(urls_bp)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
