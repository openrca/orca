import abc


class Fetcher(abc.ABC):

    @abc.abstractmethod
    def fetch_all(self):
        """Returns all entities."""
