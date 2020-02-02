from flask import Blueprint
from flask_restplus import Api

from orca.api.resources.v1 import graph as graph_ns
from orca.api.resources.v1 import ingestor as ingestor_ns


def initialize(graph):
    blueprint = Blueprint('api', __name__, url_prefix='/v1')
    api = Api(blueprint, title='ORCA API', version='0.1',)
    api.add_namespace(graph_ns.initialize(graph))
    api.add_namespace(ingestor_ns.initialize(graph))
    return blueprint
