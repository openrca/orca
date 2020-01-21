from orca.common import logger
log = logger.get_logger(__name__)


class Synchronizer(object):

    def __init__(self, graph, graph_fetcher, upstream_fetcher):
        self._graph = graph
        self._graph_fetcher = graph_fetcher
        self._upstream_fetcher = upstream_fetcher

    def synchronize(self):
        nodes_in_graph = self._build_node_lookup(self._graph_fetcher.fetch_all())
        upstream_nodes = self._build_node_lookup(self._upstream_fetcher.fetch_all())

        nodes_in_graph_ids = set(nodes_in_graph.keys())
        upstream_nodes_ids = set(upstream_nodes.keys())

        nodes_to_delete_ids = nodes_in_graph_ids.difference(upstream_nodes_ids)
        nodes_to_update_ids = nodes_in_graph_ids.difference(nodes_to_delete_ids)
        nodes_to_create_ids = upstream_nodes_ids.difference(nodes_in_graph_ids)

        for node_id in nodes_to_delete_ids:
            log.info("Delete node: %s" % node_id)
            self._graph.delete_node(nodes_in_graph[node_id])

        for node_id in nodes_to_update_ids:
            log.info("Update node: %s" % node_id)
            self._graph.update_node(upstream_nodes[node_id])

        for node_id in nodes_to_create_ids:
            log.info("Add node: %s" % node_id)
            self._graph.add_node(upstream_nodes[node_id])

    @staticmethod
    def _build_node_lookup(nodes):
        return {node.id: node for node in nodes}
