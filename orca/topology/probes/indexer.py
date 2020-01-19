import abc


class Indexer(abc.ABC):

    @abc.abstractmethod
    def get_all(self):
        """Returns proxy to all origin resources."""

    @abc.abstractmethod
    def get_by_node(self, node):
        """Returns proxy to an origin resource based on node properties."""


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
