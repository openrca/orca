from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.topology.probes.k8s import indexer as k8s_indexer
from orca.common import logger

log = logger.get_logger(__name__)


class PodProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: pod")
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'pod')
        watch.add_handler(PodHandler(self._graph))
        watch.run()


class PodHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        properties['ip'] = obj.status.pod_ip
        properties['node'] = obj.spec.node_name
        return (id, 'pod', properties)


class PodToServiceLinker(linker.K8SLinker):

    def _are_linked(self, pod, service):
        match_namespace = self._match_namespace(pod, service)
        match_selector = self._match_selector(pod, service.spec.selector)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        pod_indexer = k8s_indexer.K8SIndexer(
            k8s_client.ResourceAPI(client.CoreV1Api(), 'pod'))
        service_indexer = k8s_indexer.K8SIndexer(
            k8s_client.ResourceAPI(client.CoreV1Api(), 'service'))
        return PodToServiceLinker(graph, 'pod', pod_indexer, 'service', service_indexer)


class PodToReplicaSetLinker(linker.K8SLinker):

    def _are_linked(self, pod, replica_set):
        match_namespace = self._match_namespace(pod, replica_set)
        match_selector = self._match_selector(pod, replica_set.spec.selector.match_labels)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        pod_indexer = k8s_indexer.K8SIndexer(
            k8s_client.ResourceAPI(client.CoreV1Api(), 'pod'))
        replica_set_indexer = k8s_indexer.K8SIndexer(
            k8s_client.ResourceAPI(client.ExtensionsV1beta1Api(), 'replica_set'))
        return PodToReplicaSetLinker(graph, 'pod', pod_indexer, 'replica_set', replica_set_indexer)


class PodToNodeLinker(linker.K8SLinker):

    def _are_linked(self, pod, node):
        return pod.spec.node_name == node.metadata.name

    @staticmethod
    def create(graph, client):
        pod_indexer = k8s_indexer.K8SIndexer(
            k8s_client.ResourceAPI(client.CoreV1Api(), 'pod'))
        node_indexer = k8s_indexer.K8SIndexer(
            k8s_client.ResourceAPI(client.CoreV1Api(), 'node', namespaced=False))
        return PodToNodeLinker(graph, 'pod', pod_indexer, 'node', node_indexer)
