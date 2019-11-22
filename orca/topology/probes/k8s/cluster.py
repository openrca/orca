from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.common import logger
from orca import graph

log = logger.get_logger(__name__)


class ClusterProbe(probe.K8SProbe):

    def run(self):
        log.info("Registering root node for resource: cluster")
        node_id = graph.Graph.generate_id("cluster")
        node = graph.Graph.create_node(node_id, "cluster", {'name': "cluster"})
        self._graph.add_node(node)
