from flask_restplus import Namespace, Resource, fields

from orca.core.graph import topology

api = Namespace('graph', description='Graph API')

node_fields = api.model('Graph Node', {
    'id': fields.String,
    'label': fields.String,
    'group': fields.Integer,
    'level': fields.Integer
})

link_fields = api.model('Graph Link', {
    'source': fields.String,
    'target': fields.String,
    'strength': fields.Float,
    'distance': fields.Integer
})

graph = api.model('Graph', {
    'nodes': fields.List(fields.Nested(node_fields), attribute='nodes'),
    'links': fields.List(fields.Nested(link_fields), attribute='links')
})


@api.route('/')
class Graph(Resource):
    @api.doc('get_graph')
    @api.marshal_with(graph)
    def get(self):
        '''Show the graph topology'''
        (graph_nodes, graph_links) = topology.generate(
            num_nodes=10,
            num_masters=3,
            num_deployments=3,
            pods_per_deployment=2
        )
        return {
            'nodes': graph_nodes,
            'links': graph_links
        }
