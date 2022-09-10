from flask import Blueprint
from flask_restx import Api

from orca.api.apis.v1 import graph as graph_ns
from orca.api.apis.v1 import ingestor as ingestor_ns
from orca.api.apis.v1 import alerts as alerts_ns


def initialize(graph):
    blueprint = Blueprint('api', __name__, url_prefix='/v1')
    api = Api(blueprint, title='OpenRCA API')
    api.add_namespace(graph_ns.initialize(graph))
    api.add_namespace(ingestor_ns.initialize(graph))
    api.add_namespace(alerts_ns.initialize(graph))
    return blueprint
