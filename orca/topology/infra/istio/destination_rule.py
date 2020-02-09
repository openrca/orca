from orca.common.clients import istio
from orca.topology import linker
from orca.topology.infra.istio import linker as istio_linker
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
        properties['host'] = entity.spec.host
        return properties


class DestinationRuleToServiceLinker(linker.Linker):

    @staticmethod
    def create(graph):
        return DestinationRuleToServiceLinker(
            'destination_rule', 'service', graph, DestinationRuleToServiceMatcher())


class DestinationRuleToServiceMatcher(linker.Matcher):

    def are_linked(self, destination_rule, service):
        return istio_linker.match_host_to_service(
            destination_rule.properties.namespace, destination_rule.properties.host, service)
