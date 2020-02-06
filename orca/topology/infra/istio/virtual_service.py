from orca.common import str_utils
from orca.common.clients import istio
from orca.topology.infra.k8s import extractor, probe


class VirtualServiceProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return VirtualServiceProbe(
            'virtual_service', VirtualServiceExtractor(), graph,
            istio.ResourceProxyFactory.get(k8s_client, 'virtual_service'))


class VirtualServiceExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'virtual_service'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties
