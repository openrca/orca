from orca.common.clients import k8s
from orca.topology.infra.k8s import extractor, linker, probe


class NodeProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return NodeProbe('node', NodeExtractor(), graph, k8s.ResourceProxyFactory.get(k8s_client, 'node'))


class NodeExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'node'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        return properties


class NodeToClusterLinker(linker.Linker):

    @staticmethod
    def create(graph):
        return NodeToClusterLinker('node', 'cluster', graph, NodeToClusterMatcher())


class NodeToClusterMatcher(linker.Matcher):

    def are_linked(self, pod, node):
        return True
