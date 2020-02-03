import abc


class Extractor(abc.ABC):

    @abc.abstractmethod
    def extract(self, entity):
        """Extracts graph node from given raw entity."""
