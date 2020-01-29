from flask import Blueprint
from flask_restplus import Api

from orca.api.resources.v1.graph import api as graph_ns
from orca.api.resources.v1.ingestor import api as ingestor_ns

blueprint = Blueprint('api', __name__, url_prefix='/v1')

api = Api(
    blueprint,
    title='ORCA API',
    version='0.1',
)

api.add_namespace(graph_ns)
api.add_namespace(ingestor_ns)
