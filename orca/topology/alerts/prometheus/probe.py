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
from orca import exceptions

log = logger.get_logger(__name__)


class Probe(probe.Probe):

    """Probe for synchronizing alerts from Prometheus."""

    def __init__(self, graph, extractor, prom_client):
        super().__init__(graph)
        self._extractor = extractor
        self._prom_client = prom_client

    def run(self):
        while True:
            extended_kind = self._extractor.get_extended_kind()
            log.info("Starting sync for entity: %s", extended_kind)
            self._synchronize()
            log.info("Finished sync for entity: %s", extended_kind)
            time.sleep(60)

    def _synchronize(self):
        nodes_in_graph = self._build_node_lookup(self._get_nodes_in_graph())
        upstream_nodes = self._build_node_lookup(self._get_upstream_nodes())

        nodes_in_graph_ids = set(nodes_in_graph.keys())
        upstream_nodes_ids = set(upstream_nodes.keys())

        nodes_to_delete_ids = nodes_in_graph_ids.difference(upstream_nodes_ids)
        nodes_to_update_ids = nodes_in_graph_ids.difference(nodes_to_delete_ids)
        nodes_to_create_ids = upstream_nodes_ids.difference(nodes_in_graph)

        for node_id in nodes_to_delete_ids:
            self._graph.delete_node(nodes_in_graph[node_id])

        for node_id in nodes_to_update_ids:
            self._graph.update_node(upstream_nodes[node_id])

        for node_id in nodes_to_create_ids:
            self._graph.add_node(upstream_nodes[node_id])

    def _build_node_lookup(self, nodes):
        return {node.id: node for node in nodes}

    def _get_nodes_in_graph(self):
        return self._graph.get_nodes(
            origin=self._extractor.get_origin(), kind=self._extractor.get_kind())

    def _get_upstream_nodes(self):
        entities = self._prom_client.get_alerts()['data']['alerts']
        upstream_nodes = []
        for entity in entities:
            try:
                node = self._extractor.extract(entity)
                upstream_nodes.append(node)
            except exceptions.SourceMappingError as ex:
                log.warning("Error while processing an entity: %s", ex)
        return upstream_nodes
