from flask import Flask

from orca import api
from orca.graph import graph
from orca.graph import drivers as graph_drivers


def create_app():
    # TODO: read graph backend from config
    graph_client = graph_drivers.DriverFactory.get('neo4j')
    graph_inst = graph.Graph(graph_client)

    app = Flask(__name__)
    app.register_blueprint(api.initialize(graph_inst))
    return app
