from orca.common import str_utils
from orca.common.clients import istio
from orca.topology.infra.k8s import extractor, probe


class DestinationRuleProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return DestinationRuleProbe(
            'destination_rule', DestinationRuleExtractor(), graph,
            istio.ResourceProxyFactory.get(k8s_client, 'destination_rule'))


class DestinationRuleExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'destination_rule'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties
