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
from orca.topology import linker
from orca.topology.alerts import elastalert
from orca.topology.alerts import falco
from orca.topology.alerts import prometheus

LOG = logger.get_logger(__name__)


class IngestorResource(Resource):

    """Endpoint for ingesting events from the upstream."""

    def __init__(self, api, ingestor):
        super().__init__()
        self._ingestor = ingestor

    def post(self):
        payload = request.json
        self._ingestor.ingest(payload)


def initialize(graph):
    api = Namespace('ingestor', description='Ingestor API')
    ingestor_modules = [prometheus, falco, elastalert]
    linkers = []
    for ingestor_module in ingestor_modules:
        for ingestor_bundle in ingestor_module.get_ingestors():
            for linker_module in ingestor_bundle.linkers:
               linkers.append(linker_module.get(graph))
            api.add_resource(IngestorResource, "/%s" % ingestor_bundle.name.lower(),
                resource_class_args=(ingestor_bundle.ingestor.get(graph),))
    dispatcher = linker.EventDispatcher()
    for linker_instance in linkers:
        dispatcher.add_linker(linker_instance)
    graph.add_listener(dispatcher)
    return api
