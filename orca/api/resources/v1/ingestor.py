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

import json

from flask import request
from flask_restplus import Namespace, Resource

from orca import exceptions
from orca.common import logger
from orca.topology.alerts.elastalert import manager as es
from orca.topology.alerts.falco import manager as falco
from orca.topology.alerts.prometheus import manager as prometheus

log = logger.get_logger(__name__)


class Ingestor(Resource):

    """Base class for alert ingestors."""

    def __init__(self, api, entity_handler):
        super().__init__()
        self._entity_handler = entity_handler

    def post(self):
        payload = request.json
        log.debug("Ingested an entity: %s", json.dumps(payload))
        self._ingest(payload)

    def _ingest(self, entity):
        try:
            self._entity_handler.handle_event(entity)
        except exceptions.OrcaError as ex:
            log.warning("Error while processing an entity: %s", ex)


class Prometheus(Ingestor):

    """Prometheus ingest endpoint."""

    def post(self):
        payload = request.json
        log.debug(json.dumps(payload))
        for alert in payload['alerts']:
            self._ingest(alert)


class Falco(Ingestor):

    """Falco ingest endpoint."""


class Elastalert(Ingestor):

    """Elastalert ingest endpoint."""


def initialize(graph):
    api = Namespace('ingestor', description='Ingestor API')
    api.add_resource(
        Prometheus, '/prometheus',
        resource_class_args=[prometheus.initialize_handler(graph)])
    api.add_resource(
        Falco, '/falco',
        resource_class_args=[falco.initialize_handler(graph)])
    api.add_resource(
        Elastalert, '/elastalert',
        resource_class_args=[es.initialize_handler(graph)])
    return api
