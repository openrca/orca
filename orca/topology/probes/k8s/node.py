
from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import linker, probe
from orca.topology.probes.k8s import synchronizer as k8s_sync

log = logger.get_logger(__name__)


class NodeProbe(probe.Probe):

    @staticmethod
    def create(graph, client):
        extractor = NodeExtractor()
        synchronizer = k8s_sync.SynchronizerFactory.get_synchronizer(
            graph, client, 'node', extractor)
        handler = probe.KubeHandler(graph, extractor)
        watcher = k8s_client.ResourceWatch(client.CoreV1Api(), 'node', namespaced=False)
        watcher.add_handler(handler)
        return NodeProbe('node', synchronizer, watcher)


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
