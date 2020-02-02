from flask_restplus import Namespace, Resource, fields


class Graph(Resource):

    def __init__(self, api, graph):
        super().__init__()
        self._graph = graph

    def get(self):
        return


def initialize(graph):
    return Namespace('graph', description='Graph API')
