from flask_script import Manager

from orca.app import create_app

app = create_app()

manager = Manager(app)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
