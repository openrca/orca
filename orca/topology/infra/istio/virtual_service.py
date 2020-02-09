import copy

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
        properties['hosts'] = entity.spec.hosts.copy()
        properties['http'] = copy.deepcopy(entity.spec.http) if entity.spec.http else []
        properties['tls'] = copy.deepcopy(entity.spec.tls) if entity.spec.tls else []
        properties['tcp'] = copy.deepcopy(entity.spec.tcp) if entity.spec.tcp else []
        return properties


class VirtualServiceToGatewayLinker(linker.Linker):

    @staticmethod
    def create(graph):
        return VirtualServiceToGatewayLinker(
            'virtual_service', 'gateway', graph, VirtualServiceToGatewayMatcher())


class VirtualServiceToGatewayMatcher(linker.Matcher):

    def are_linked(self, virtual_service, gateway):
        return self._match_gateway(virtual_service, gateway)

    def _match_gateway(self, virtual_service, gateway):
        return gateway.properties.name in virtual_service.properties.gateways


class VirtualServiceToServiceLinker(linker.Linker):

    @staticmethod
    def create(graph):
        return VirtualServiceToServiceLinker(
            'virtual_service', 'service', graph, VirtualServiceToServiceMatcher())


class VirtualServiceToServiceMatcher(linker.Matcher):

    def are_linked(self, virtual_service, service):
        namespace = virtual_service.properties.namespace
        if self._match_route_destination(
           namespace, virtual_service.properties.http, service):
            return True
        if self._match_route_destination(
           namespace, virtual_service.properties.tls, service):
            return True
        if self._match_route_destination(
           namespace, virtual_service.properties.tcp, service):
            return True
        return False

    def _match_route_destination(self, namespace, routes, service):
        for route in routes:
            for route_dest in route.route:
                if self._match_host_to_service(namespace, route_dest.destination.host, service):
                    return True
        return False

    def _match_host_to_service(self, namespace, host, service):
        host_parts = host.split('.')
        service_name = host_parts[0]
        service_namespace = host_parts[1] if len(host_parts) > 1 else namespace
        match_name = service_name == service.properties.name
        match_namespace = service_namespace == service.properties.namespace
        return match_name and match_namespace
