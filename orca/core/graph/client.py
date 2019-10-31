from abc import ABC, abstractmethod


class Node(object):
    pass


class Link(object):
    pass


class Client(ABC):

    """Abstract Graph DB client."""

    @abstractmethod
    def get_nodes(self):
        """Get all graph nodes."""

    @abstractmethod
    def get_node(self):
        """Get graph node details."""

    @abstractmethod
    def create_node(self):
        """Create a graph node."""

    @abstractmethod
    def update_node(self):
        """Update a graph node."""

    @abstractmethod
    def delete_node(self):
        """Delete a graph node."""

    @abstractmethod
    def get_links(self):
        """Get all graph links."""

    @abstractmethod
    def get_link(self):
        """Get graph link details."""

    @abstractmethod
    def create_link(self):
        """Create a graph link."""

    @abstractmethod
    def update_link(self):
        """Update a graph link."""

    @abstractmethod
    def delete_link(self):
        """Delete a graph link."""

    @abstractmethod
    def get_node_links(self):
        """Get graph node links."""