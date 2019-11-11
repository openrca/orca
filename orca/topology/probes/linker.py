from abc import ABC, abstractmethod

from orca import graph


class Linker(ABC):

    def __init__(self, graph):
        self._graph = graph

    @staticmethod
    def _build_link_lookup(links):
        return {link.id: link for link in links}

    def link(self, node):
        current_links = Linker._build_link_lookup(
            self._get_current_links(node))
        new_links = Linker._build_link_lookup(
            self._get_new_links(node))
        for link_id, link in new_links.items():
            if link_id not in current_links:
                self._graph.add_link(link)
            else:
                self._graph.update_link(link)
        for link_id, link in current_links.items():
            if link_id not in new_links:
                self._graph.delete_link(link)

    def _get_current_links(self, node):
        return self._graph.get_node_links(node)

    @abstractmethod
    def _get_new_links(self, node):
        """Returns a snapshot of graph links for a given node."""
