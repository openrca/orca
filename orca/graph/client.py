from abc import ABC, abstractmethod

# from orca.graph import drivers


class GraphObject(ABC):

    def __init__(self, id, metadata):
        self.id = id
        self.metadata = metadata


class Node(GraphObject):

    def __init__(self, id, metadata):
        super().__init__(id, metadata)

    def __repr__(self):
        return "<Node id=%s metadata=%s>" % (self.id, self.metadata)


class Link(GraphObject):

    def __init__(self, id, metadata, source, target):
        super().__init__(id, metadata)
        self.source = source
        self.target = target

    def __repr__(self):
        return "<Link id=%s metadata=%s source=%s target=%s>" % (
            self.id, self.metadata, self.source.id, self.target.id)


class Client(ABC):

    """Abstract Graph DB client."""

    @abstractmethod
    def get_nodes(self, metadata):
        """Get all graph nodes."""

    @abstractmethod
    def get_node(self, id):
        """Get graph node details."""

    @abstractmethod
    def create_node(self, id, metadata):
        """Create a graph node."""

    @abstractmethod
    def update_node(self, id, metadata):
        """Update a graph node."""

    @abstractmethod
    def delete_node(self, id):
        """Delete a graph node."""

    @abstractmethod
    def get_links(self, metadata):
        """Get all graph links."""

    @abstractmethod
    def get_link(self, id):
        """Get graph link details."""

    @abstractmethod
    def create_link(self, id, source_id, target_id, metadata):
        """Create a graph link."""

    @abstractmethod
    def update_link(self, id, metadata):
        """Update a graph link."""

    @abstractmethod
    def delete_link(self, id):
        """Delete a graph link."""


# class ClientFactory(object):

#     @staticmethod
#     def get_client(backend='neo4j'):
#         if backend == 'neo4j':
#             uri = None  # config.get('NEO4J_URI')
#             return drivers.Neo4jClient(uri)
