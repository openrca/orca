from abc import ABC, abstractmethod

from orca.topology.probes import linker
from orca import graph
from orca.common import logger

log = logger.get_logger(__name__)


class K8SListener(graph.EventListener):

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


class K8SLinker(linker.Linker, ABC):

    def __init__(self, graph, resource_a_api, resource_b_api):
        super().__init__(graph)
        self._resource_a_api = resource_a_api
        self._resource_b_api = resource_b_api

    def _get_new_links(self, node):
        links = []
        links.extend(self._get_ab_links(node))
        links.extend(self._get_ba_links(node))
        return links

    def _get_ab_links(self, node_a):
        links = []
        resource_a = self._resource_a_api.get(
            node_a.metadata['namespace'],
            node_a.metadata['name'])
        if not resource_a:
            return links
        for resource_b in self._resource_b_api.get_all():
            node_b_id = resource_b.metadata.uid
            node_b = self._graph.get_node(node_b_id)
            if not node_b:
                continue
            if self._are_linked(resource_a, resource_b):
                link = graph.Graph.create_link({}, node_a, node_b)
                links.append(link)
        return links

    def _get_ba_links(self, node_b):
        links = []
        resource_b = self._resource_b_api.get(
            node_b.metadata['namespace'],
            node_b.metadata['name'])
        if not resource_b:
            return links
        for resource_a in self._resource_a_api.get_all():
            node_a_id = resource_a.metadata.uid
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
