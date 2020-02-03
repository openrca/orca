from orca.k8s import client as k8s
from orca.topology.infra.k8s import extractor, probe


class StatefulSetProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return StatefulSetProbe('stateful_set', StatefulSetExtractor(), graph,
                               k8s.ResourceProxy.get(k8s_client, 'stateful_set'))


class StatefulSetExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'stateful_set'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties
