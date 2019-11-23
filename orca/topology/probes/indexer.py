import abc


class Indexer(abc.ABC):

    @abc.abstractmethod
    def get_all(self):
        """Returns proxy to all origin resources."""

    @abc.abstractmethod
    def get_by_node(self, node):
        """Returns proxy to an origin resource based on node metadata."""


class ResourceProxy(abc.ABC):

    def __init__(self, resource):
        self._resource = resource

    @abc.abstractmethod
    def get_id(self):
        """Returns ID of a resource."""

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._resource, attr)


class GraphIndexer(Indexer):

    def __init__(self, graph, resource_kind):
        super().__init__()
        self._graph = graph
        self._resource_kind = resource_kind

    def get_all(self):
        nodes = self._graph.get_nodes(kind=self._resource_kind)
        return [GraphResourceProxy(node) for node in nodes]

    def get_by_node(self, node):
        node = self._graph.get_node(id=node.id, kind=self._resource_kind)
        if node:
            return GraphResourceProxy(node)


class GraphResourceProxy(ResourceProxy):

    def get_id(self):
        return self._resource.id
