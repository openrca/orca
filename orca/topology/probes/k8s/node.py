
from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher
from orca.topology.probes.k8s import extractor, linker, probe

log = logger.get_logger(__name__)


class NodeProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: node")
        extractor = NodeExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'node', namespaced=False)
        watch.add_handler(handler)
        watch.run()


class NodeExtractor(extractor.Extractor):

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
