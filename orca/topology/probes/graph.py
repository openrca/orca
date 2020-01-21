from orca.topology.probes import indexer


class Indexer(indexer.Indexer):

    def __init__(self, graph, resource_kind):
        super().__init__()
        self._graph = graph
        self._resource_kind = resource_kind

    def get_all(self):
        return self._graph.get_nodes(kind=self._resource_kind)
