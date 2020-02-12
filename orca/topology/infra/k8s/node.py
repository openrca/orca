from orca.topology import linker
from orca.topology.infra.k8s import extractor


class NodeExtractor(extractor.Extractor):

    def get_kind(self):
        return 'node'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        return properties


class NodeToClusterMatcher(linker.Matcher):

    def are_linked(self, pod, node):
        return True
