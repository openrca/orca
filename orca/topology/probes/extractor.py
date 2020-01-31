import abc

from orca.graph import graph


class Extractor(abc.ABC):

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
        """Extracts kind from given entity object."""

    @abc.abstractmethod
    def extract_properties(self, entity):
        """Extracts properties from given entity object."""


class AlertExtractor(Extractor):

    def extract_properties(self, entity):
        return {
            'name': self.extract_name(entity),
            'source_labels': self.extract_source_labels(entity),
            'status': self.extract_status(entity),
            'severity': self.extract_severity(entity),
            'message': self.extract_message(entity)
        }

    @abc.abstractmethod
    def extract_name(self, entity):
        """Extracts name from given entity object."""

    @abc.abstractmethod
    def extract_source_labels(self, entity):
        """Extracts source labels from given entity object."""

    @abc.abstractmethod
    def extract_status(self, entity):
        """Extracts status from given entity object."""

    @abc.abstractmethod
    def extract_severity(self, entity):
        """Extracts severity from given entity object."""

    @abc.abstractmethod
    def extract_message(self, entity):
        """Extracts message from given entity object."""
