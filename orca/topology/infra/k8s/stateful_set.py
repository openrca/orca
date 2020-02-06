from orca.k8s import client as k8s
from orca.topology.infra.k8s import extractor, probe


class StatefulSetProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return StatefulSetProbe('stateful_set', StatefulSetExtractor(), graph,
                                k8s.ResourceProxyFactory.get(k8s_client, 'stateful_set'))


class StatefulSetExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'stateful_set'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties
