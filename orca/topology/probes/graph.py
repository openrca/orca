from orca.topology.probes import indexer


class Indexer(indexer.Indexer):

    def __init__(self, graph, resource_kind):
        super().__init__()
        self._graph = graph
        self._resource_kind = resource_kind

    def get_all(self):
        nodes = self._graph.get_nodes(kind=self._resource_kind)
        return [ResourceProxy(node) for node in nodes]

    def get_by_node(self, node):
        node = self._graph.get_node(id=node.id, kind=self._resource_kind)
        if node:
            return ResourceProxy(node)


class ResourceProxy(indexer.ResourceProxy):

    def get_id(self):
        return self._resource.id
