from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes import graph as graph_fetcher
from orca.topology.probes.k8s import linker, probe

log = logger.get_logger(__name__)


class ReplicaSetExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties


class ReplicaSetProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: replica_set")
        extractor = ReplicaSetExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.ExtensionsV1beta1Api(), 'replica_set')
        watch.add_handler(handler)
        watch.run()


class ReplicaSetToDeploymentLinker(linker.Linker):

    def _are_linked(self, replica_set, deployment):
        match_namespace = self._match_namespace(replica_set, deployment)
        match_selector = self._match_selector(replica_set, deployment.properties.selector)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        replica_set_fetcher = graph_fetcher.Fetcher(graph, 'replicaset')
        deployment_fetcher = graph_fetcher.Fetcher(graph, 'deployment')
        return ReplicaSetToDeploymentLinker(
            graph, 'replicaset', replica_set_fetcher, 'deployment', deployment_fetcher)
