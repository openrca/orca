from orca.common import logger
from orca.common.clients.k8s import client as k8s
from orca.topology import probe

log = logger.get_logger(__name__)


class Probe(probe.Probe, k8s.EventHandler):

    def __init__(self, graph, extractor, k8s_client):
        super().__init__(graph)
        self._extractor = extractor
        self._k8s_client = k8s_client

    def run(self):
        extended_kind = self._extractor.get_extended_kind()
        log.info("Starting sync for entity: %s", extended_kind)
        self._synchronize()
        log.info("Finished sync for entity: %s", extended_kind)
        log.info("Starting watch on entity: %s", extended_kind)
        self._start_watch()

    def on_added(self, entity):
        node = self._extractor.extract(entity)
        self._graph.add_node(node)

    def on_updated(self, entity):
        node = self._extractor.extract(entity)
        self._graph.update_node(node)

    def on_deleted(self, entity):
        node = self._extractor.extract(entity)
        self._graph.delete_node(node)

    def _synchronize(self):
        nodes_in_graph = self._build_node_lookup(self._get_nodes_in_graph())
        upstream_nodes = self._build_node_lookup(self._get_upstream_nodes())

        nodes_in_graph_ids = set(nodes_in_graph.keys())
        upstream_nodes_ids = set(upstream_nodes.keys())

        nodes_to_delete_ids = nodes_in_graph_ids.difference(upstream_nodes_ids)
        nodes_to_update_ids = nodes_in_graph_ids.difference(nodes_to_delete_ids)
        nodes_to_create_ids = upstream_nodes_ids.difference(nodes_in_graph_ids)

        for node_id in nodes_to_delete_ids:
            self._graph.delete_node(nodes_in_graph[node_id])

        for node_id in nodes_to_update_ids:
            self._graph.update_node(upstream_nodes[node_id])

        for node_id in nodes_to_create_ids:
            self._graph.add_node(upstream_nodes[node_id])

    def _build_node_lookup(self, nodes):
        return {node.id: node for node in nodes}

    def _get_nodes_in_graph(self):
        return self._graph.get_nodes(
            origin=self._extractor.get_origin(), kind=self._extractor.get_kind())

    def _get_upstream_nodes(self):
        entities = self._k8s_client.get_all()
        return [self._extractor.extract(entity) for entity in entities]

    def _start_watch(self):
        self._k8s_client.watch(handler=self)
