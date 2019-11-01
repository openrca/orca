from flask import Flask

from orca.api import blueprint as api_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app
