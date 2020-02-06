from orca.common.clients import istio
from orca.topology.infra.k8s import extractor, linker, probe


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
        properties['gateways'] = entity.spec.gateways.copy()
        return properties


class VirtualServiceToGatewayLinker(linker.Linker):

    @staticmethod
    def create(graph):
        return VirtualServiceToGatewayLinker(
            'virtual_service', 'gateway', graph, VirtualServiceToGatewayMatcher())


class VirtualServiceToGatewayMatcher(linker.Matcher):

    def are_linked(self, virtual_service, gateway):
        match_namespace = self._match_namespace(virtual_service, gateway)
        match_gateway = self._match_gateway(virtual_service, gateway)
        return match_namespace and match_gateway

    def _match_gateway(self, virtual_service, gateway):
        return gateway.properties.name in virtual_service.properties.gateways
