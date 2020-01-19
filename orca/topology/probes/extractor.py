import abc

from orca.graph import graph


class Extractor(object):

    def extract(self, entity):
        node_id = self.extract_id(entity)
        kind = self.extract_kind(entity)
        properties = self.extract_properties(entity)
        return graph.Node(node_id, properties, kind)

    @abc.abstractmethod
    def extract_id(self, entity):
        """Extracts ID from given entity object."""

    @abc.abstractmethod
    def extract_kind(self, entity):
        """Extracts kind of given entity object."""

    @abc.abstractmethod
    def extract_properties(self, entity):
        """Extracts properties from given entity object."""
