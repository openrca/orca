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

import time

from orca.common import logger
from orca.graph import graph
from orca.topology import probe

log = logger.get_logger(__name__)


class Probe(probe.Probe):

    def __init__(self, graph, origin, kind):
        super().__init__(graph)
        self._origin = origin
        self._kind = kind

    def run(self):
        while True:
            alert_nodes = self._graph.get_nodes(origin=self._origin, kind=self._kind)
            for alert_node in alert_nodes:
                source_mapping = alert_node.properties.source_mapping
                if not source_mapping:
                    continue
                source_nodes = self._graph.get_nodes(
                    kind=source_mapping.kind, properties=source_mapping.properties)
                for source_node in source_nodes:
                    link = graph.Graph.create_link({}, source_node, alert_node)
                    self._graph.add_link(link)
            time.sleep(10)


class EntityHandler(object):

    def __init__(self, graph, extractor):
        self._graph = graph
        self._extractor = extractor

    def handle(self, entity):
        node = self._extractor.extract(entity)
        self._graph.add_node(node)
