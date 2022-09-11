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

from orca.common import config, logger
from orca.topology import linker
from orca.topology import alerts

CONFIG = config.CONFIG
LOG = logger.get_logger(__name__)


class IngestorResource(Resource):

    """Endpoint for ingesting events from the upstream."""

    def __init__(self, api, ingestor):
        super().__init__()
        self._ingestor = ingestor

    def post(self):
        payload = request.json
        self._ingestor.ingest(payload)


class IngestorRegistry(object):

    """Registers ingestor API resources and graph linkers."""

    def __init__(self, api, graph, event_dispatcher):
        self._api = api
        self._graph = graph
        self._event_dispatcher = event_dispatcher

    def register(self, ingestor_bundle):
        for linker_module in ingestor_bundle.linkers:
            linker_instance = linker_module.get(self._graph)
            self._event_dispatcher.add_linker(linker_instance)

        ingestor = ingestor_bundle.ingestor.get(self._graph)
        endpoint = "/%s" % ingestor_bundle.name.lower()

        self._api.add_resource(IngestorResource, endpoint, resource_class_args=(ingestor,))


def initialize(graph):
    api = Namespace("ingestor", description="Ingestor API")

    event_dispatcher = linker.EventDispatcher()
    graph.add_listener(event_dispatcher)
    ingestor_registry = IngestorRegistry(api, graph, event_dispatcher)

    ingestor_modules = []

    if CONFIG.ingestors.prometheus.enabled:
        ingestor_modules.append(alerts.prometheus)

    if CONFIG.ingestors.falco.enabled:
        ingestor_modules.append(alerts.falco)

    if CONFIG.ingestors.elastalert.enabled:
        ingestor_modules.append(alerts.elastalert)

    for ingestor_module in ingestor_modules:
        for ingestor_bundle in ingestor_module.get_ingestors():
            ingestor_registry.register(ingestor_bundle)
    return api
