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


properties_fields = Model('Properties', {
    'name': fields.String(attribute='properties.source_mapping.properties.name'),
    'namespace': fields.String(attribute='properties.source_mapping.properties.namespace', default="n/a")
})


source_fields = Model('Source', {
    'origin': fields.String(attribute='properties.source_mapping.origin'),
    'kind': fields.String(attribute='properties.source_mapping.kind'),
    'properties': fields.Nested(properties_fields)
})


alerts_fields = Model('Alert Node', {
    'id': fields.String,
    'origin': fields.String,
    'name': fields.String(attribute='properties.name'),
    'message': fields.String(attribute='properties.message'),
    'severity': fields.String(attribute='properties.severity'),
    'source': fields.Nested(source_fields),
    'created_at': fields.String,
    'updated_at': fields.String
})


class Alerts(Resource):

    def __init__(self, api, graph):
        super().__init__()
        self._graph = graph

    def get(self):
        properties = {'kind': 'alert'}
        return marshal(self._graph.get_nodes(properties=properties), alerts_fields)


def initialize(graph):
    api = Namespace('alerts', description='Alerts API')
    api.add_resource(Alerts, '/', resource_class_args=[graph])
    return api
