from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import probe

log = logger.get_logger(__name__)


class Probe(probe.Probe, k8s_client.EventHandler):

    def __init__(self, kind, extractor, graph, k8s_client):
        self._kind = kind
        self._extractor = extractor
        self._graph = graph
        self._k8s_client = k8s_client

    def run(self):
        self.synchronize()
        self.start_watch()

    def synchronize(self):
        nodes_in_graph = self._build_node_lookup(self._graph.get_nodes(kind=self._kind))
        upstream_nodes = self._build_node_lookup(self._get_nodes_from_upstream())

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

    def start_watch(self):
        self._k8s_client.watch(handler=self)

    def on_added(self, entity):
        node = self._extractor.extract(entity)
        self._graph.add_node(node)

    def on_updated(self, entity):
        node = self._extractor.extract(entity)
        self._graph.update_node(node)

    def on_deleted(self, entity):
        node = self._extractor.extract(entity)
        self._graph.delete_node(node)

    def _get_nodes_from_upstream(self):
        entities = self._k8s_client.get_all()
        return [self._extractor.extract(entity) for entity in entities]

    @staticmethod
    def _build_node_lookup(nodes):
        return {node.id: node for node in nodes}
