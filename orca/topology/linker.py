import abc

from orca.graph import graph


class Dispatcher(graph.EventListener):

    """Listens for graph events and triggers node linking on node updates."""

    def __init__(self):
        self._linkers = {}

    def add_linker(self, linker):
        self._linkers.setdefault(linker.source_kind, []).append(linker)
        self._linkers.setdefault(linker.target_kind, []).append(linker)

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

    """Links pair of nodes based on the matching condition."""

    def __init__(self, source_kind, target_kind, graph, matcher):
        super().__init__()
        self.source_kind = source_kind
        self.target_kind = target_kind
        self._graph = graph
        self._matcher = matcher

    def link(self, node):
        current_links = self._build_link_lookup(self._get_current_links(node))
        new_links = self._build_link_lookup(self._get_new_links(node))

        current_links_ids = set(current_links.keys())
        new_links_ids = set(new_links.keys())

        links_to_delete_ids = current_links_ids.difference(new_links_ids)
        links_to_update_ids = current_links_ids.difference(links_to_delete_ids)
        links_to_create_ids = new_links_ids.difference(current_links_ids)

        for link_id in links_to_delete_ids:
            self._graph.delete_link(current_links[link_id])

        for link_id in links_to_update_ids:
            self._graph.update_link(new_links[link_id])

        for link_id in links_to_create_ids:
            self._graph.add_link(new_links[link_id])

    def _get_current_links(self, node):
        target_kind = self._get_target_kind(node)
        return self._graph.get_node_links(node, kind=target_kind)

    def _get_target_kind(self, node):
        if node.kind == self.source_kind:
            return self.target_kind
        return self.source_kind

    def _get_new_links(self, node):
        linked_nodes = self._get_linked_nodes(node)
        links = []
        for linked_node in linked_nodes:
            link = graph.Graph.create_link({}, node, linked_node)
            links.append(link)
        return links

    def _get_linked_nodes(self, node):
        if node.kind == self.source_kind:
            return self._get_linked_from_source(node)
        else:
            return self._get_linked_from_target(node)

    def _get_linked_from_source(self, source_node):
        linked_nodes = []
        for target_node in self._graph.get_nodes(kind=self.target_kind):
            if self._matcher.are_linked(source_node, target_node):
                linked_nodes.append(target_node)
        return linked_nodes

    def _get_linked_from_target(self, target_node):
        linked_nodes = []
        for source_node in self._graph.get_nodes(kind=self.source_kind):
            if self._matcher.are_linked(source_node, target_node):
                linked_nodes.append(source_node)
        return linked_nodes

    def _build_link_lookup(self, links):
        return {link.id: link for link in links}


class Matcher(abc.ABC):

    @abc.abstractmethod
    def are_linked(self, noda_a, node_b):
        """Determines whether two graph nodes are interconnected."""
