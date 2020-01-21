import abc


class Fetcher(abc.ABC):

    @abc.abstractmethod
    def fetch_all(self):
        """Returns proxy to all upstream resources."""
