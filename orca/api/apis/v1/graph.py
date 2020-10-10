# Copyright 2020 OpenRCA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask_restx import Model, Namespace, Resource, fields, marshal, reqparse

from orca.api.schema import GraphSchema


query_parser = reqparse.RequestParser()
query_parser.add_argument('time_point', type=int)


class Graph(Resource):

    def __init__(self, api, graph):
        super().__init__()
        self._graph = graph

    def get(self):
        args = query_parser.parse_args()
        graph_data = {
            'nodes': self._graph.get_nodes(time_point=args['time_point']),
            'links': self._graph.get_links(time_point=args['time_point'])
        }
        graph_schema = GraphSchema()
        result = graph_schema.dump(graph_data)
        return result, 200


def initialize(graph):
    api = Namespace('graph', description='Graph API')
    api.add_resource(Graph, '/', resource_class_args=[graph])
    return api
