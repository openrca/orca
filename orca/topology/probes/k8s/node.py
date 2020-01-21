
from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher
from orca.topology.probes import synchronizer as sync
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import fetcher as k8s_fetcher
from orca.topology.probes.k8s import linker, probe
from orca.topology.probes.k8s import synchronizer as k8s_sync

log = logger.get_logger(__name__)


class NodeProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S sync on resource: node")
        extractor = NodeExtractor()
        synchronizer = k8s_sync.SynchronizerFactory.get_synchronizer(
            self._graph, self._client, 'node', extractor)
        synchronizer.synchronize()
        log.info("Finished K8S sync on resource: node")
        log.info("Starting K8S watch on resource: node")
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'node', namespaced=False)
        watch.add_handler(handler)
        watch.run()


class NodeExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'node'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        return properties


class NodeToClusterLinker(linker.Linker):

    @staticmethod
    def create(graph, client):
        fetcher_a = fetcher.GraphFetcher(graph, 'node')
        fetcher_b = fetcher.GraphFetcher(graph, 'cluster')
        matcher = NodeToClusterMatcher()
        return NodeToClusterLinker(
            graph, 'node', fetcher_a, 'cluster', fetcher_b, matcher)


class NodeToClusterMatcher(linker.Matcher):

    def are_linked(self, pod, node):
        return True
