import cotyledon

from orca.topology.probes import k8s as k8s_probe
from orca.topology.probes.k8s import client as k8s_client
from orca import graph as graph_client


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()
        graph = self._init_graph()
        self._add_k8s_probes(graph)

    def _init_graph(self):
        # TODO: read graph backend from config
        graph_backend = 'neo4j'
        return graph_client.ClientFactory.get_client(graph_backend)

    def _add_k8s_probes(self, graph):
        client = k8s_client.ClientFactory.get_client()
        for probe in k8s_probe.PROBES:
            self.add(probe, workers=1, args=(graph, client))
