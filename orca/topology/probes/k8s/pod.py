from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import indexer as k8s_indexer
from orca.topology.probes.k8s import linker, probe

log = logger.get_logger(__name__)


class PodExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['ip'] = entity.status.pod_ip
        properties['node'] = entity.spec.node_name
        return properties


class PodProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: pod")
        extractor = PodExtractor()
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'pod')
        watch.add_handler(PodHandler(self._graph, extractor))
        watch.run()


class PodHandler(probe.K8SResourceHandler):
    pass


class PodToServiceLinker(linker.Linker):

    def _are_linked(self, pod, service):
        match_namespace = self._match_namespace(pod, service)
        match_selector = self._match_selector(pod, service.spec.selector)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        pod_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'pod')
        service_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'service')
        return PodToServiceLinker(graph, 'pod', pod_indexer, 'service', service_indexer)


class PodToReplicaSetLinker(linker.Linker):

    def _are_linked(self, pod, replica_set):
        match_namespace = self._match_namespace(pod, replica_set)
        match_selector = self._match_selector(pod, replica_set.spec.selector.match_labels)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        pod_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'pod')
        replica_set_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'replica_set')
        return PodToReplicaSetLinker(graph, 'pod', pod_indexer, 'replica_set', replica_set_indexer)


class PodToNodeLinker(linker.Linker):

    def _are_linked(self, pod, node):
        return pod.spec.node_name == node.metadata.name

    @staticmethod
    def create(graph, client):
        pod_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'pod')
        node_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'node')
        return PodToNodeLinker(graph, 'pod', pod_indexer, 'node', node_indexer)
