from abc import ABC, abstractmethod

from orca import graph
from orca.common import logger
from orca.topology.probes import linker

log = logger.get_logger(__name__)


class K8SLinker(linker.Linker, ABC):

    def __init__(self, graph, kind_a, indexer_a, kind_b, indexer_b):
        super().__init__(graph, kind_a, kind_b)
        self._indexer_a = indexer_a
        self._indexer_b = indexer_b

    def _get_new_links(self, node):
        links = []
        links.extend(self._get_ab_links(node))
        links.extend(self._get_ba_links(node))
        return links

    def _get_ab_links(self, node_a):
        links = []
        resource_a = self._indexer_a.get_by_node(node_a)
        if not resource_a:
            return links
        for resource_b in self._indexer_b.get_all():
            node_b_id = resource_b.get_id()
            node_b = self._graph.get_node(node_b_id)
            if not node_b:
                continue
            if self._are_linked(resource_a, resource_b):
                link = graph.Graph.create_link({}, node_a, node_b)
                links.append(link)
        return links

    def _get_ba_links(self, node_b):
        links = []
        resource_b = self._indexer_b.get_by_node(node_b)
        if not resource_b:
            return links
        for resource_a in self._indexer_a.get_all():
            node_a_id = resource_a.get_id()
            node_a = self._graph.get_node(node_a_id)
            if not node_a:
                continue
            if self._are_linked(resource_a, resource_b):
                link = graph.Graph.create_link({}, node_a, node_b)
                links.append(link)
        return links

    @abstractmethod
    def _are_linked(self, resource_a, resource_b):
        """Determines whether two K8S resources are interconnected."""

    def _match_namespace(self, resource_a, resource_b):
        return resource_a.metadata.namespace == resource_b.metadata.namespace

    def _match_selector(self, resource, selector):
        labels = resource.metadata.labels
        if selector and labels:
            return all(item in labels.items() for item in selector.items())
        return False
