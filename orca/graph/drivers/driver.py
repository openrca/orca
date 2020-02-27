import abc


class Driver(abc.ABC):

    """Abstract Graph DB driver."""

    @abc.abstractmethod
    def get_nodes(self, kind, properties):
        """Gets all graph nodes."""

    @abc.abstractmethod
    def get_node(self, id, kind, properties):
        """Gets graph node details."""

    @abc.abstractmethod
    def add_node(self, node):
        """Creates a graph node."""

    @abc.abstractmethod
    def update_node(self, node):
        """Updates a graph node."""

    @abc.abstractmethod
    def delete_node(self, node):
        """Deletes a graph node."""

    @abc.abstractmethod
    def get_links(self, properties):
        """Gets all graph links."""

    @abc.abstractmethod
    def get_link(self, id, properties):
        """Gets graph link details."""

    @abc.abstractmethod
    def add_link(self, link):
        """Creates a graph link."""

    @abc.abstractmethod
    def update_link(self, link):
        """Updates a graph link."""

    @abc.abstractmethod
    def delete_link(self, link):
        """Deletes a graph link."""

    @abc.abstractmethod
    def get_node_links(self, node, kind):
        """Gets links connected to a node."""
