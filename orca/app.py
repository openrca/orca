from flask import Flask

from orca.apis import blueprint as api_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app
