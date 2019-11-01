from flask import Blueprint
from flask_restplus import Api

from orca.api.graph import api as graph_ns

blueprint = Blueprint('api', __name__, url_prefix='/v1')

api = Api(
    blueprint,
    title='ORCA API',
    version='0.1',
)

api.add_namespace(graph_ns)
