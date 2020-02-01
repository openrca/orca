from orca.k8s import client as k8s
from orca.topology.k8s import extractor, linker, probe


class ReplicaSetProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return ReplicaSetProbe('replica_set', ReplicaSetExtractor(), graph,
                               k8s.ResourceProxy.get(k8s_client, 'replica_set'))


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
    def create(graph):
        return ReplicaSetToDeploymentLinker('replica_set', 'deployment', graph,
                                            ReplicaSetToDeploymentMatcher())


class ReplicaSetToDeploymentMatcher(linker.Matcher):

    def are_linked(self, replica_set, deployment):
        match_namespace = self._match_namespace(replica_set, deployment)
        match_selector = self._match_selector(replica_set, deployment.properties.selector)
        return match_namespace and match_selector
