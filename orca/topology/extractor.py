import abc


class Extractor(abc.ABC):

    @abc.abstractmethod
    def get_origin(self):
        """Returns origin of extracted entities."""

    @abc.abstractmethod
    def get_kind(self):
        """Returns kind of extracted entities."""

    @abc.abstractmethod
    def extract(self, entity):
        """Extracts graph node from given raw entity."""

    def get_extended_kind(self):
        return "%s/%s" % (self.get_origin(), self.get_kind())
