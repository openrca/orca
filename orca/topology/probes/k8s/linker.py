import abc

from orca.graph import graph
from orca.common import logger
from orca.topology.probes import linker

log = logger.get_logger(__name__)


class Linker(linker.Linker, abc.ABC):

    def __init__(self, graph, kind_a, indexer_a, kind_b, indexer_b):
        super().__init__(graph, kind_a, kind_b)
        self._indexer_a = indexer_a
        self._indexer_b = indexer_b

    def _get_new_links(self, node):
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

    def _match_namespace(self, node_a, node_b):
        return node_a.properties.namespace == node_b.properties.namespace

    def _match_selector(self, node, selector):
        labels = node.properties.labels
        if selector and labels:
            return all(item in labels.items() for item in selector.items())
        return False
