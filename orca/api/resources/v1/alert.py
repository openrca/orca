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

alerts_fields = Model('Alert Node', {
    'id': fields.String,
    'origin': fields.String,
    'name': fields.String(attribute='properties.name'),
    'message': fields.String(attribute='properties.message'),
    'severity': fields.String(attribute='properties.severity'),
    'source': {
        'origin': fields.String(attribute='properties.source_mapping.origin'),
        'kind': fields.String(attribute='properties.source_mapping.kind'),
        'properties': {
            'name': fields.String(attribute='properties.source_mapping.properties.name'),
            'namespace': fields.String(attribute='properties.source_mapping.properties.namespace', default="n/a")
        }
    },
    'created_at': fields.String,
    'updated_at': fields.String
})


class Alerts(Resource):

    def __init__(self, api, graph):
        super().__init__()
        self._alerts = graph

    def get(self):
        return marshal(self._alerts.get_nodes(kind='alert'), alerts_fields)


def initialize(graph):
    api = Namespace('alerts', description='Alerts API')
    api.add_resource(Alerts, '/', resource_class_args=[graph])
    return api
