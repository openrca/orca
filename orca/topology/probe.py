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

import abc
import time

import cotyledon

from orca import exceptions
from orca.common import config, logger
from orca.graph import graph
from orca.topology import linker, upstream

CONFIG = config.CONFIG
LOG = logger.get_logger(__name__)


class ProbeRunner(cotyledon.Service):

    """Runs entity probe from given probe bundle."""

    def __init__(self, worker_id, probe_bundle, graph_lock):
        super().__init__(worker_id)
        self._worker_id = worker_id
        self._probe_bundle = probe_bundle
        self._graph_lock = graph_lock
        self.__graph = None

    @property
    def _graph(self):
        if not self.__graph:
            self.__graph = graph.Graph.get(self._graph_lock)
        return self.__graph

    def run(self):
        probe = self._initialize_probe()
        linkers = self._initialize_linkers()
        self._setup_event_dispatcher(linkers)
        probe.run()

    def _initialize_probe(self):
        probe_module = self._probe_bundle.probe
        return probe_module.get(self._graph)

    def _initialize_linkers(self):
        linkers = []
        linker_modules = self._probe_bundle.linkers
        for linker_module in linker_modules:
            linkers.append(linker_module.get(self._graph))
        return linkers

    def _setup_event_dispatcher(self, linkers):
        event_dispatcher = linker.EventDispatcher()
        for linker_instance in linkers:
            event_dispatcher.add_linker(linker_instance)
        self._graph.add_listener(event_dispatcher)


class Probe(abc.ABC):

    """Base class for entity probes."""

    def __init__(self, graph):
        super().__init__()
        self._graph = graph

    @abc.abstractmethod
    def run(self):
        """Starts entity probe."""

    @classmethod
    def get(cls, graph):
        return cls(graph)


class PullProbe(Probe):

    """Periodically pulls all entities from the upstream into the graph."""

    def __init__(self, graph, upstream_proxy, extractor, synchronizer, resync_period=60):
        super().__init__(graph)
        self._upstream_proxy = upstream_proxy
        self._extractor = extractor
        self._synchronizer = synchronizer
        self._resync_period = resync_period

    def run(self):
        extended_kind = self._extractor.get_extended_kind()
        while True:
            LOG.info("Starting sync for entity: %s", extended_kind)
            start_time = time.time()
            self._synchronize()
            sync_time = time.time() - start_time
            LOG.info("Finished sync for entity: %s (%.2f seconds)", extended_kind, sync_time)
            time.sleep(self._resync_period)

    def _synchronize(self):
        nodes_in_graph = self._get_nodes_in_graph()
        upstream_nodes = self._get_upstream_nodes()
        self._synchronizer.synchronize(nodes_in_graph, upstream_nodes)

    def _get_nodes_in_graph(self):
        properties = {"origin": self._extractor.origin, "kind": self._extractor.kind}
        return self._graph.get_nodes(properties=properties)

    def _get_upstream_nodes(self):
        entities = self._upstream_proxy.get_all()
        upstream_nodes = []
        for entity in entities:
            try:
                node = self._extractor.extract(entity)
                upstream_nodes.append(node)
            except exceptions.OrcaError as ex:
                LOG.warning("Error while processing an entity: %s", ex)
        return upstream_nodes


class PushProbe(Probe, upstream.EventHandler):

    """Consumes events pushed by the upstream."""

    def __init__(self, graph, upstream_proxy, extractor):
        super().__init__(graph)
        self._upstream_proxy = upstream_proxy
        self._extractor = extractor

    def run(self):
        extended_kind = self._extractor.get_extended_kind()
        LOG.info("Consuming events for entity: %s", extended_kind)
        self._upstream_proxy.get_events(handler=self)

    def on_added(self, entity):
        node = self._extractor.extract(entity)
        self._graph.add_node(node)

    def on_updated(self, entity):
        node = self._extractor.extract(entity)
        self._graph.update_node(node)

    def on_deleted(self, entity):
        node = self._extractor.extract(entity)
        self._graph.delete_node(node.id)
