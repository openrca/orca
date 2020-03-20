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

from orca.common import logger
from orca.common.clients.k8s import client as k8s
from orca.topology import probe

LOG = logger.get_logger(__name__)


class Probe(probe.Probe, k8s.EventHandler):

    """Probe for Kubernetes entities."""

    def __init__(self, graph, extractor, synchronizer, k8s_client):
        super().__init__(graph)
        self._extractor = extractor
        self._synchronizer = synchronizer
        self._k8s_client = k8s_client

    def run(self):
        extended_kind = self._extractor.get_extended_kind()
        LOG.info("Starting sync for entity: %s", extended_kind)
        self._synchronize()
        LOG.info("Finished sync for entity: %s", extended_kind)
        LOG.info("Starting watch on entity: %s", extended_kind)
        self._start_watch()

    def on_added(self, entity):
        node = self._extractor.extract(entity)
        self._graph.add_node(node)

    def on_updated(self, entity):
        node = self._extractor.extract(entity)
        self._graph.update_node(node)

    def on_deleted(self, entity):
        node = self._extractor.extract(entity)
        self._graph.delete_node(node)

    def _synchronize(self):
        nodes_in_graph = self._get_nodes_in_graph()
        upstream_nodes = self._get_upstream_nodes()
        self._synchronizer.synchronize(nodes_in_graph, upstream_nodes, create=False)

    def _get_nodes_in_graph(self):
        return self._graph.get_nodes(
            origin=self._extractor.get_origin(), kind=self._extractor.get_kind())

    def _get_upstream_nodes(self):
        entities = self._k8s_client.get_all()
        return [self._extractor.extract(entity) for entity in entities]

    def _start_watch(self):
        self._k8s_client.watch(handler=self)
