from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import indexer as k8s_indexer
from orca.topology.probes.k8s import linker, probe

log = logger.get_logger(__name__)


class ReplicaSetProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: replica_set")
        watch = k8s_client.ResourceWatch(self._client.ExtensionsV1beta1Api(), 'replica_set')
        watch.add_handler(ReplicaSetHandler(self._graph))
        watch.run()


class ReplicaSetHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        properties['replicas'] = obj.spec.replicas
        return (id, 'replica_set', properties)


class ReplicaSetToDeploymentLinker(linker.K8SLinker):

    def _are_linked(self, replica_set, deployment):
        match_namespace = self._match_namespace(replica_set, deployment)
        match_selector = self._match_selector(replica_set, deployment.spec.selector.match_labels)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        replica_set_indexer = k8s_indexer.K8SIndexerFactory.get_indexer(client, 'replica_set')
        deployment_indexer = k8s_indexer.K8SIndexerFactory.get_indexer(client, 'deployment')
        return ReplicaSetToDeploymentLinker(
            graph, 'replica_set', replica_set_indexer, 'deployment', deployment_indexer)
