from flask_restplus import Namespace, Resource, fields

api = Namespace('graph', description='Graph API')

graph = api.model('Graph', {
    'topology': fields.String(required=True, description='Graph topology'),
})

GRAPH = {'topology': 'TEST'}


@api.route('/')
class Graph(Resource):
    @api.doc('get_graph')
    @api.marshal_with(graph)
    def get(self):
        '''Show the graph'''
        return GRAPH
