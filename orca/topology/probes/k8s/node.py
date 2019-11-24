
from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import graph as graph_indexer
from orca.topology.probes.k8s import indexer as k8s_indexer
from orca.topology.probes.k8s import linker, probe

log = logger.get_logger(__name__)


class NodeProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: node")
        watch = k8s_client.ResourceWatch(
            self._client.CoreV1Api(), 'node', namespaced=False)
        watch.add_handler(NodeHandler(self._graph))
        watch.run()


class NodeHandler(probe.K8SResourceHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        return (id, 'node', properties)


class NodeToClusterLinker(linker.Linker):

    def _are_linked(self, node, cluster):
        return True

    @staticmethod
    def create(graph, client):
        node_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'node')
        cluster_indexer = graph_indexer.Indexer(graph, 'cluster')
        return NodeToClusterLinker(graph, 'node', node_indexer, 'cluster', cluster_indexer)
