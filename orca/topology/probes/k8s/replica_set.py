from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import indexer as k8s_indexer
from orca.topology.probes.k8s import linker, probe

log = logger.get_logger(__name__)


class ReplicaSetExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['replicas'] = entity.spec.replicas
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
        match_selector = self._match_selector(replica_set, deployment.spec.selector.match_labels)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        replica_set_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'replica_set')
        deployment_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'deployment')
        return ReplicaSetToDeploymentLinker(
            graph, 'replica_set', replica_set_indexer, 'deployment', deployment_indexer)
