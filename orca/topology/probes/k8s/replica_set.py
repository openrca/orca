from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes import fetcher
from orca.topology.probes.k8s import linker, probe

log = logger.get_logger(__name__)


class ReplicaSetProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: replica_set")
        extractor = ReplicaSetExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.ExtensionsV1beta1Api(), 'replica_set')
        watch.add_handler(handler)
        watch.run()


class ReplicaSetExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties


class ReplicaSetToDeploymentLinker(linker.Linker):

    @staticmethod
    def create(graph, client):
        fetcher_a = fetcher.GraphFetcher(graph, 'replicaset')
        fetcher_b = fetcher.GraphFetcher(graph, 'deployment')
        matcher = ReplicaSetToDeploymentMatcher()
        return ReplicaSetToDeploymentLinker(
            graph, 'replicaset', fetcher_a, 'deployment', fetcher_b, matcher)


class ReplicaSetToDeploymentMatcher(linker.Matcher):

    def are_linked(self, replica_set, deployment):
        match_namespace = self._match_namespace(replica_set, deployment)
        match_selector = self._match_selector(replica_set, deployment.properties.selector)
        return match_namespace and match_selector
