from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import linker, probe
from orca.topology.probes.k8s import synchronizer as k8s_sync

log = logger.get_logger(__name__)


class ReplicaSetProbe(probe.Probe):

    @staticmethod
    def create(graph, client):
        extractor = ReplicaSetExtractor()
        synchronizer = k8s_sync.SynchronizerFactory.get_synchronizer(
            graph, client, 'replica_set', extractor)
        handler = probe.KubeHandler(graph, extractor)
        watcher = k8s_client.ResourceWatch(client.ExtensionsV1beta1Api(), 'replica_set')
        watcher.add_handler(handler)
        return ReplicaSetProbe('replica_set', synchronizer, watcher)


class ReplicaSetExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'replica_set'

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
        fetcher_a = fetcher.GraphFetcher(graph, 'replica_set')
        fetcher_b = fetcher.GraphFetcher(graph, 'deployment')
        matcher = ReplicaSetToDeploymentMatcher()
        return ReplicaSetToDeploymentLinker(
            graph, 'replica_set', fetcher_a, 'deployment', fetcher_b, matcher)


class ReplicaSetToDeploymentMatcher(linker.Matcher):

    def are_linked(self, replica_set, deployment):
        match_namespace = self._match_namespace(replica_set, deployment)
        match_selector = self._match_selector(replica_set, deployment.properties.selector)
        return match_namespace and match_selector
