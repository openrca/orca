from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class ReplicaSetExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'replica_set'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties


class ReplicaSetToDeploymentMatcher(linker.Matcher):

    def are_linked(self, replica_set, deployment):
        match_namespace = k8s_linker.match_namespace(replica_set, deployment)
        match_selector = k8s_linker.match_selector(replica_set, deployment.properties.selector)
        return match_namespace and match_selector
