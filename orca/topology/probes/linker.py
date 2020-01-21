import abc

from orca.graph import graph


class GraphListener(graph.EventListener):

    def __init__(self):
        self._linkers = {}

    def add_linker(self, linker):
        self._linkers.setdefault(linker.kind_a, []).append(linker)
        self._linkers.setdefault(linker.kind_b, []).append(linker)

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
        if node.kind in self._linkers:
            for linker in self._linkers[node.kind]:
                linker.link(node)


class Linker(abc.ABC):

    def __init__(self, graph, kind_a, indexer_a, kind_b, indexer_b):
        self.kind_a = kind_a
        self.kind_b = kind_b
        self._graph = graph
        self._indexer_a = indexer_a
        self._indexer_b = indexer_b

    def link(self, node):
        links_in_graph = self._build_link_lookup(self._get_links_in_graph(node))
        upstream_links = self._build_link_lookup(self._get_upstream_links(node))

        links_in_graph_ids = set(links_in_graph.keys())
        upstream_links_ids = set(upstream_links.keys())

        links_to_delete_ids = links_in_graph_ids.difference(upstream_links_ids)
        links_to_update_ids = links_in_graph_ids.difference(links_to_delete_ids)
        links_to_create_ids = upstream_links_ids.difference(links_in_graph_ids)

        for link_id in links_to_delete_ids:
            self._graph.delete_link(links_in_graph[link_id])

        for link_id in links_to_update_ids:
            self._graph.update_link(upstream_links[link_id])

        for link_id in links_to_create_ids:
            self._graph.add_link(upstream_links[link_id])

    def _get_links_in_graph(self, node):
        target_kind = self._get_target_kind(node)
        return self._graph.get_node_links(node, kind=target_kind)

    def _get_target_kind(self, node):
        return self.kind_a if node.kind == self.kind_b else self.kind_b

    def _get_upstream_links(self, node):
        if node.kind == self.kind_a:
            return self._get_ab_links(node)
        else:
            return self._get_ba_links(node)

    def _get_ab_links(self, node_a):
        links = []
        for node_b in self._indexer_b.get_all():
            if self._are_linked(node_a, node_b):
                link = graph.Graph.create_link({}, node_a, node_b)
                links.append(link)
        return links

    def _get_ba_links(self, node_b):
        links = []
        for node_a in self._indexer_a.get_all():
            if self._are_linked(node_a, node_b):
                link = graph.Graph.create_link({}, node_a, node_b)
                links.append(link)
        return links

    @abc.abstractmethod
    def _are_linked(self, node_a, node_b):
        """Determines whether two graph nodes are interconnected."""

    @staticmethod
    def _build_link_lookup(links):
        return {link.id: link for link in links}
