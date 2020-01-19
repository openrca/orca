
from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import graph as graph_indexer
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import indexer as k8s_indexer
from orca.topology.probes.k8s import linker, probe

log = logger.get_logger(__name__)


class NodeExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        return properties


class NodeProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: node")
        extractor = NodeExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'node', namespaced=False)
        watch.add_handler(handler)
        watch.run()


class NodeToClusterLinker(linker.Linker):

    def _are_linked(self, node, cluster):
        return True

    @staticmethod
    def create(graph, client):
        node_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'node')
        cluster_indexer = graph_indexer.Indexer(graph, 'cluster')
        return NodeToClusterLinker(graph, 'node', node_indexer, 'cluster', cluster_indexer)
