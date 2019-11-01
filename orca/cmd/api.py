from orca.api.app import create_app


def main():
    app = create_app()
    app.run(host='0.0.0.0')