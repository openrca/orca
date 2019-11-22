import abc

from orca import graph


class GraphListener(graph.EventListener):

    def __init__(self):
        self._linkers = []

    def add_linker(self, linker):
        self._linkers.append(linker)

    def on_node_added(self, node):
        self._link_node(node)

    def on_node_updated(self, node):
        self._link_node(node)

    def on_node_deleted(self, node):
        return

    def on_link_added(self, link):
        return

    def on_link_updated(self, link):
        return

    def on_link_deleted(self, link):
        return

    def _link_node(self, node):
        for linker in self._linkers:
            linker.link(node)


class Linker(abc.ABC):

    def __init__(self, graph, kind_a, kind_b):
        self._graph = graph
        self._kind_a = kind_a
        self._kind_b = kind_b

    @property
    def kind_a(self):
        return self._kind_a

    @property
    def kind_b(self):
        return self._kind_b

    def link(self, node):
        if not self._is_node_linkable(node):
            return
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

    def _is_node_linkable(self, node):
        if node.kind == self._kind_a:
            return True
        if node.kind == self._kind_b:
            return True
        return False

    def _get_current_links(self, node):
        links = self._graph.get_node_links(node)
        target_node_kind = self._kind_a
        if node.kind == self._kind_a:
            target_node_kind = self._kind_b
        return filter(
            lambda link: (link.target.kind == target_node_kind),
            links)

    @abc.abstractmethod
    def _get_new_links(self, node):
        """Returns a snapshot of graph links for a given node."""

    @staticmethod
    def _build_link_lookup(links):
        return {link.id: link for link in links}
