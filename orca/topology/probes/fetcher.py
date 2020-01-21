import abc


class Fetcher(abc.ABC):

    @abc.abstractmethod
    def fetch_all(self):
        """Returns all entities."""


class GraphFetcher(Fetcher):

    def __init__(self, graph, resource_kind):
        super().__init__()
        self._graph = graph
        self._resource_kind = resource_kind

    def fetch_all(self):
        return self._graph.get_nodes(kind=self._resource_kind)
