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

node_fields = Model('Alert Node', {
    'id': fields.String,
    'origin': fields.String,
    'properties': {
        'name': fields.String(attribute='properties.name'),
        'kind': fields.String(attribute='properties.source_mapping.kind'),
        'instance': fields.String(attribute='properties.source_mapping.properties.name'),
        'namespace': fields.String(attribute='properties.source_mapping.properties.namespace', default="n/a"),
	'message': fields.String(attribute='properties.message'),
	'severity': fields.String(attribute='properties.severity')
    }
})

alerts_fields = Model('Alerts', {
    'alerts': fields.List(
        fields.Nested(node_fields), attribute='nodes')
})


class Alerts(Resource):

    def __init__(self, api, alerts):
        super().__init__()
        self._alerts = alerts

    def get(self):
        data = {
            'nodes': self._alerts.get_nodes(kind='alert'),
        }
        return marshal(data, alerts_fields)


def initialize(alerts):
    api = Namespace('alerts', description='Alerts API')
    api.add_resource(Alerts, '/', resource_class_args=[alerts])
    return api
