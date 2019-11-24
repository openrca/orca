import abc


class Client(abc.ABC):

    """Abstract Graph DB client."""

    @abc.abstractmethod
    def get_nodes(self, kind, metadata):
        """Get all graph nodes."""

    @abc.abstractmethod
    def get_node(self, id, kind, metadata):
        """Get graph node details."""

    @abc.abstractmethod
    def add_node(self, node):
        """Create a graph node."""

    @abc.abstractmethod
    def update_node(self, node):
        """Update a graph node."""

    @abc.abstractmethod
    def delete_node(self, node):
        """Delete a graph node."""

    @abc.abstractmethod
    def get_links(self, metadata):
        """Get all graph links."""

    @abc.abstractmethod
    def get_link(self, id, metadata):
        """Get graph link details."""

    @abc.abstractmethod
    def add_link(self, link):
        """Create a graph link."""

    @abc.abstractmethod
    def update_link(self, link):
        """Update a graph link."""

    @abc.abstractmethod
    def delete_link(self, link):
        """Delete a graph link."""

    @abc.abstractmethod
    def get_node_links(self, node, kind):
        """Get links connected to a node."""
