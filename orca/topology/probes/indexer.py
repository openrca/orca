import abc


class Indexer(abc.ABC):

    @abc.abstractmethod
    def get_all(self):
        """Returns proxy to all upstream resources."""
