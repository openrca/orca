import cotyledon
from orca.graph import drivers as graph_drivers
from orca.graph.graph import Graph
from orca.k8s import client as k8s
from orca.topology.probes import k8s as k8s_probe
from orca.topology.probes import linker, probe


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()
        graph = self._init_graph()
        self._add_k8s_probes(graph)

    def _init_graph(self):
        # TODO: read graph backend from config
        graph_client = graph_drivers.ClientFactory.get_client('neo4j')
        return Graph(graph_client)

    def _add_k8s_probes(self, graph):
        k8s_client = k8s.ClientFactory.get_client()

        linker_dispatcher = linker.Dispatcher()
        for k8s_linker in k8s_probe.LINKERS:
            linker_dispatcher.add_linker(k8s_linker.create(graph))

        graph.add_listener(linker_dispatcher)

        for probe_klass in k8s_probe.PROBES:
            probe_inst = probe_klass.create(graph, k8s_client)
            self.add(probe.ProbeService, workers=1, args=(probe_inst,))
