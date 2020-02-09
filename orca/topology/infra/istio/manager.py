from orca.common.clients import istio, k8s
from orca.topology import linker
from orca.topology.infra.istio import (destination_rule, gateway,
                                       virtual_service)
from orca.topology.infra.k8s import probe


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            kind='virtual_service',
            extractor=virtual_service.VirtualServiceExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'virtual_service')),
        probe.Probe(
            kind='destination_rule',
            extractor=destination_rule.DestinationRuleExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'destination_rule')),
        probe.Probe(
            kind='gateway',
            extractor=gateway.GatewayExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'gateway'))]


def initialize_linkers(graph):
    return [
        linker.Linker(
            kind_a='virtual_service',
            kind_b='gateway',
            graph=graph,
            matcher=virtual_service.VirtualServiceToGatewayMatcher()),
        linker.Linker(
            kind_a='virtual_service',
            kind_b='gateway',
            graph=graph,
            matcher=virtual_service.VirtualServiceToServiceMatcher()),
        linker.Linker(
            kind_a='destination_rule',
            kind_b='service',
            graph=graph,
            matcher=destination_rule.DestinationRuleToServiceMatcher())]
