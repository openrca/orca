import abc


class Extractor(abc.ABC):

    def __init__(self, origin, kind):
        self.origin = origin
        self.kind = kind

    @abc.abstractmethod
    def extract(self, entity):
        """Extracts graph node from given raw entity."""
