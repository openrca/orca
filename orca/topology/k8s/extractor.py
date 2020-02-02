import abc

from orca.graph import graph
from orca.topology import extractor


class Extractor(extractor.Extractor):

    def extract(self, entity):
        node_id = self.extract_id(entity)
        kind = self.extract_kind(entity)
        properties = self.extract_properties(entity)
        return graph.Node(node_id, properties, kind)

    def extract_id(self, entity):
        return entity.metadata.uid

    def extract_kind(self, entity):
        return entity.kind.lower()

    @abc.abstractmethod
    def extract_properties(self, entity):
        """Extracts properties from given K8S object."""
