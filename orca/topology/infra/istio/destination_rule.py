from orca.common.clients import istio
from orca.topology.infra.k8s import extractor, linker, probe


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
        properties['host'] = entity.spec.host
        return properties


class DestinationRuleToServiceLinker(linker.Linker):

    @staticmethod
    def create(graph):
        return DestinationRuleToServiceLinker(
            'destination_rule', 'service', graph, DestinationRuleToServiceMatcher())


class DestinationRuleToServiceMatcher(linker.Matcher):

    def are_linked(self, destination_rule, service):
        return self._match_host_to_service(
            destination_rule.properties.namespace, destination_rule.properties.host, service)


    def _match_host_to_service(self, namespace, host, service):
        host_parts = host.split('.')
        service_name = host_parts[0]
        service_namespace = host_parts[1] if len(host_parts) > 1 else namespace
        match_name = service_name == service.properties.name
        match_namespace = service_namespace == service.properties.namespace
        return match_name and match_namespace
