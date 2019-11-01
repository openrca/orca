from abc import ABC, abstractmethod


class GraphObject(ABC):

    def __init__(self, id, metadata):
        self._id = id
        self._metadata = metadata

    @property
    def id(self):
        return self._id

    @property
    def metadata(self):
        return self._metadata


class Node(GraphObject):

    def __init__(self, id, metadata, type):
        super().__init__(id, metadata)
        self._type = type

    @property
    def type(self):
        return self._type


class Link(GraphObject):

    def __init__(self, id, metadata, source, target):
        super().__init__(id, metadata)
        self._source = source
        self._target = target

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target


class Client(ABC):

    """Abstract Graph DB client."""

    @abstractmethod
    def get_nodes(self):
        """Get all graph nodes."""

    @abstractmethod
    def get_node(self, id):
        """Get graph node details."""

    @abstractmethod
    def create_node(self, node):
        """Create a graph node."""

    @abstractmethod
    def update_node(self, node):
        """Update a graph node."""

    @abstractmethod
    def delete_node(self, id):
        """Delete a graph node."""

    @abstractmethod
    def get_links(self):
        """Get all graph links."""

    @abstractmethod
    def get_link(self, id):
        """Get graph link details."""

    @abstractmethod
    def create_link(self, link):
        """Create a graph link."""

    @abstractmethod
    def update_link(self, link):
        """Update a graph link."""

    @abstractmethod
    def delete_link(self, id):
        """Delete a graph link."""

    @abstractmethod
    def get_node_links(self, id):
        """Get graph node links."""


class ClientFactory(object):

    @staticmethod
    def get_client(backend='neo4j'):
        pass
