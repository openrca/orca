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

from flask_restx import Model, Namespace, Resource, fields, marshal


node_fields = Model('Graph Node', {
    'id': fields.String,
    'origin': fields.String,
    'kind': fields.String,
    'properties': {
        'name': fields.String(attribute='properties.name'),
        'namespace': fields.String(attribute='properties.namespace', default="n/a")
    }
})

link_fields = Model('Graph Link', {
    'id': fields.String,
    'source': fields.String(attribute='source.id'),
    'target': fields.String(attribute='target.id')
})

graph_fields = Model('Graph', {
    'nodes': fields.List(
        fields.Nested(node_fields), attribute='nodes'),
    'links': fields.List(
        fields.Nested(link_fields), attribute='links')
})


class Graph(Resource):

    def __init__(self, api, graph):
        super().__init__()
        self._graph = graph

    def get(self):
        data = {
            'nodes': self._graph.get_nodes(),
            'links': self._graph.get_links()
        }
        return marshal(data, graph_fields)


def initialize(graph):
    api = Namespace('graph', description='Graph API')
    api.add_resource(Graph, '/', resource_class_args=[graph])
    return api
