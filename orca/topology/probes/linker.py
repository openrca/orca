import abc

from orca.graph import graph


class Dispatcher(graph.EventListener):

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

    def __init__(self, kind_a, kind_b, graph, matcher):
        super().__init__()
        self.kind_a = kind_a
        self.kind_b = kind_b
        self._graph = graph
        self._matcher = matcher

    def link(self, node):
        old_links = self._build_link_lookup(self._get_old_links(node))
        new_links = self._build_link_lookup(self._get_new_links(node))

        old_links_ids = set(old_links.keys())
        new_links_ids = set(new_links.keys())

        links_to_delete_ids = old_links_ids.difference(new_links_ids)
        links_to_update_ids = old_links_ids.difference(links_to_delete_ids)
        links_to_create_ids = new_links_ids.difference(old_links_ids)

        for link_id in links_to_delete_ids:
            self._graph.delete_link(old_links[link_id])

        for link_id in links_to_update_ids:
            self._graph.update_link(new_links[link_id])

        for link_id in links_to_create_ids:
            self._graph.add_link(new_links[link_id])

    def _get_old_links(self, node):
        target_kind = self._get_target_kind(node)
        return self._graph.get_node_links(node, kind=target_kind)

    def _get_target_kind(self, node):
        return self.kind_b if node.kind == self.kind_a else self.kind_a

    def _get_new_links(self, node):
        linked_nodes = []
        if node.kind == self.kind_a:
            linked_nodes.extend(self._get_ab_links(node))
        else:
            linked_nodes.extend(self._get_ba_links(node))
        links = []
        for linked_node in linked_nodes:
            link = graph.Graph.create_link({}, node, linked_node)
            links.append(link)
        return links

    def _get_ab_links(self, node_a):
        linked_nodes = []
        for node_b in self._graph.get_nodes(kind=self.kind_b):
            if self._matcher.are_linked(node_a, node_b):
                linked_nodes.append(node_b)
        return linked_nodes

    def _get_ba_links(self, node_b):
        linked_nodes = []
        for node_a in self._graph.get_nodes(kind=self.kind_a):
            if self._matcher.are_linked(node_a, node_b):
                linked_nodes.append(node_a)
        return linked_nodes

    @staticmethod
    def _build_link_lookup(links):
        return {link.id: link for link in links}


class Matcher(abc.ABC):

    @abc.abstractmethod
    def are_linked(self, noda_a, node_b):
        """Determines whether two graph nodes are interconnected."""
