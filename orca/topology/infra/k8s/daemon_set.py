from orca.common.clients import k8s
from orca.topology.infra.k8s import extractor, probe


class DaemonSetProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return DaemonSetProbe('daemon_set', DaemonSetExtractor(), graph,
                              k8s.ResourceProxyFactory.get(k8s_client, 'daemon_set'))


class DaemonSetExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'daemon_set'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['selector'] = entity.spec.selector.match_labels
        return properties
