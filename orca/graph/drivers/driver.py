import abc


class Driver(abc.ABC):

    """Abstract Graph DB driver."""

    @abc.abstractmethod
    def get_nodes(self, kind, properties):
        """Get all graph nodes."""

    @abc.abstractmethod
    def get_node(self, id, kind, properties):
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
    def get_links(self, properties):
        """Get all graph links."""

    @abc.abstractmethod
    def get_link(self, id, properties):
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
