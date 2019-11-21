from abc import ABC, abstractmethod


class Client(ABC):

    """Abstract Graph DB client."""

    @abstractmethod
    def get_nodes(self, kind, metadata):
        """Get all graph nodes."""

    @abstractmethod
    def get_node(self, id, kind, metadata):
        """Get graph node details."""

    @abstractmethod
    def add_node(self, node):
        """Create a graph node."""

    @abstractmethod
    def update_node(self, node):
        """Update a graph node."""

    @abstractmethod
    def delete_node(self, node):
        """Delete a graph node."""

    @abstractmethod
    def get_links(self, kind, metadata):
        """Get all graph links."""

    @abstractmethod
    def get_link(self, id, kind, metadata):
        """Get graph link details."""

    @abstractmethod
    def add_link(self, link):
        """Create a graph link."""

    @abstractmethod
    def update_link(self, link):
        """Update a graph link."""

    @abstractmethod
    def delete_link(self, link):
        """Delete a graph link."""

    @abstractmethod
    def get_node_links(self, node):
        """Get links connected to a node."""
