from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import probe

log = logger.get_logger(__name__)


class Probe(probe.Probe):

    def __init__(self, entity_kind, synchronizer, watcher):
        self._entity_kind = entity_kind
        self._synchronizer = synchronizer
        self._watcher = watcher

    def run(self):
        log.info("Starting sync on entity kind: %s", self._entity_kind)
        self._synchronizer.synchronize()
        log.info("Finished sync on entity kind: %s", self._entity_kind)

        log.info("Starting watch on entity kind: %s", self._entity_kind)
        self._watcher.run()


class KubeHandler(k8s_client.EventHandler):

    def __init__(self, graph, extractor):
        self._graph = graph
        self._extractor = extractor

    def on_added(self, entity):
        node = self._extractor.extract(entity)
        self._graph.add_node(node)

    def on_updated(self, entity):
        node = self._extractor.extract(entity)
        self._graph.update_node(node)

    def on_deleted(self, entity):
        node = self._extractor.extract(entity)
        self._graph.delete_node(node)
