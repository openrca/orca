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

from orca.common import config, logger
from orca.common.clients.kiali import client as kiali
from orca.graph import graph
from orca.topology import probe

CONFIG = config.CONFIG
LOG = logger.get_logger(__name__)


class ServiceGraphProbe(probe.Probe):

    """Probe for synchronizing service graph from Kiali."""

    def __init__(self, graph, kiali_client, resync_period=60):
        super().__init__(graph)
        self._kiali_client = kiali_client
        self._resync_period = resync_period

    def run(self):
        while True:
            LOG.info("Starting sync for Kiali service graph")
            start_time = time.time()
            self._synchronize()
            sync_time = time.time() - start_time
            LOG.info("Finished sync for Kiali service graph (%.2f seconds)", sync_time)
            time.sleep(self._resync_period)

    def _synchronize(self):
        namespaces = self._get_namespaces()
        nodes, edges = self._get_service_graph(namespaces)
        service_mapping = self._build_service_mapping(nodes)
        self._synchronize_links(edges, service_mapping)

    def _get_namespaces(self):
        return [namespace["name"] for namespace in self._kiali_client.list_namespaces()]

    def _get_service_graph(self, namespaces):
        service_graph = self._kiali_client.graph_namespaces(namespaces)
        node_elements = service_graph["elements"]["nodes"]
        edge_elements = service_graph["elements"]["edges"]
        nodes = [element["data"] for element in node_elements]
        edges = [element["data"] for element in edge_elements]
        return (nodes, edges)

    def _build_service_mapping(self, nodes):
        service_mapping = {}
        for node in nodes:
            if node["nodeType"] == "service":
                service_mapping[node["id"]] = {
                    "name": node["service"],
                    "namespace": node["namespace"],
                }
        return service_mapping

    def _synchronize_links(self, edges, service_mapping):
        for edge in edges:
            source_id = edge["source"]
            target_id = edge["target"]
            source_mapping = service_mapping.get(source_id)
            target_mapping = service_mapping.get(target_id)
            if source_mapping and target_mapping:
                source_node = self._get_service(source_mapping)
                target_node = self._get_service(target_mapping)
                properties = self._extract_edge_properties(edge)
                if source_node and target_node:
                    self._link_services(source_node, target_node, properties)

    def _get_service(self, mapping):
        properties = {"origin": "kubernetes", "kind": "service", "properties": mapping}
        matches = self._graph.get_nodes(properties=properties)
        if matches:
            return matches[0]

    def _extract_edge_properties(self, edge):
        return {"protocol": edge["traffic"]["protocol"]}

    def _link_services(self, source_node, target_node, properties):
        link = graph.Graph.create_link(properties, source_node, target_node)
        if self._graph.get_link(link.id):
            self._graph.update_link(link)
        else:
            self._graph.add_link(link)

    @classmethod
    def get(cls, graph):
        kiali_client = kiali.KialiClient.get(
            url=CONFIG.probes.kiali.url,
            username=CONFIG.probes.kiali.username,
            password=CONFIG.probes.kiali.password,
        )
        return cls(
            graph=graph, kiali_client=kiali_client, resync_period=CONFIG.probes.kiali.resync_period
        )
