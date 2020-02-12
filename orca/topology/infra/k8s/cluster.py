from orca.graph import graph
from orca.common import logger
from orca.topology import probe

log = logger.get_logger(__name__)


class ClusterProbe(probe.Probe):

    def run(self):
        log.info("Registering root node for entity: cluster")
        node_id = graph.Graph.generate_id("cluster")
        node = graph.Graph.create_node(node_id, {'name': "cluster"}, "kubernetes", "cluster")
        self._graph.add_node(node)
