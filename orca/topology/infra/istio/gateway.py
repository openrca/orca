from orca.common.clients import istio
from orca.topology.infra.k8s import extractor, probe


class GatewayProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return GatewayProbe(
            'gateway', GatewayExtractor(), graph,
            istio.ResourceProxyFactory.get(k8s_client, 'gateway'))


class GatewayExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'gateway'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties
