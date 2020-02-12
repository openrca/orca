import abc

from orca.graph import graph
from orca.topology import extractor


class Extractor(extractor.Extractor):

    def extract(self, entity):
        node_id = self._extract_id(entity)
        origin = self._extract_origin(entity)
        kind = self._extract_kind(entity)
        properties = self._extract_properties(entity)
        return graph.Node(node_id, properties, origin, kind)

    def _extract_id(self, entity):
        return entity.metadata.uid

    def _extract_origin(self, entity):
        return "kubernetes"

    def _extract_kind(self, entity):
        return entity.kind.lower()

    @abc.abstractmethod
    def _extract_properties(self, entity):
        """Extracts properties from given K8S object."""
