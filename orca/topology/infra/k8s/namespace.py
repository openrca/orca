from orca.topology import linker
from orca.topology.infra.k8s import extractor


class NamespaceExtractor(extractor.Extractor):

    def get_kind(self):
        return 'namespace'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['labels'] = None
        if entity.metadata.labels:
            properties['labels'] = entity.metadata.labels.copy()
        properties['phase'] = entity.status.phase
        return properties


class NamespaceMatcher(linker.Matcher):

    def are_linked(self, obj, namespace):
        return namespace.properties.name == obj.properties.namespace
