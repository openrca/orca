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

from flask import request
from flask_restx import Namespace, Resource

from orca.api.schema import AlertSchema, AlertQuerySchema


class Alerts(Resource):
    def __init__(self, api, graph):
        super().__init__()
        self._graph = graph

    def get(self):
        query_schema = AlertQuerySchema()
        query = query_schema.load(request.args)
        timepoint = query["time_point"]
        include_deleted = query["deleted"]
        alert_data = self._graph.get_nodes(
            time_point=timepoint, properties={"kind": "alert"}, include_deleted=include_deleted
        )
        alert_schema = AlertSchema(many=True)
        result = alert_schema.dump(alert_data)
        return result, 200


def initialize(graph):
    api = Namespace("alerts", description="Alerts API")
    api.add_resource(Alerts, "/", resource_class_args=[graph])
    return api
