from orca.graph import client


class Neo4j(client.Client):

    """Neo4j Graph DB client."""

    def get_nodes(self):
        """Get all graph nodes."""
        pass

    def get_node(self, id):
        """Get graph node details."""
        pass

    def create_node(self, node):
        """Create a graph node."""
        pass

    def update_node(self, node):
        """Update a graph node."""
        pass

    def delete_node(self, id):
        """Delete a graph node."""
        pass

    def get_links(self):
        """Get all graph links."""
        pass

    def get_link(self, id):
        """Get graph link details."""
        pass

    def create_link(self, link):
        """Create a graph link."""
        pass

    def update_link(self, link):
        """Update a graph link."""
        pass

    def delete_link(self, id):
        """Delete a graph link."""
        pass

    def get_node_links(self, id):
        """Get graph node links."""
        pass