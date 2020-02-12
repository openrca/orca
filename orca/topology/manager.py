import cotyledon

from orca.graph import drivers as graph_drivers
from orca.graph.graph import Graph
from orca.topology import linker, probe
from orca.topology.alerts.elastalert import manager as es
from orca.topology.alerts.falco import manager as falco
from orca.topology.alerts.prometheus import manager as prom
from orca.topology.infra.istio import manager as istio
from orca.topology.infra.k8s import manager as k8s
from orca.topology.infra.kiali import manager as kiali


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()

    def initialize(self):
        graph = self._init_graph()
        linker_dispatcher = linker.Dispatcher()
        graph.add_listener(linker_dispatcher)

        probe_managers = [k8s, istio, prom, falco, es, kiali]
        for probe_manager in probe_managers:
            for probe_inst in probe_manager.initialize_probes(graph):
                self.add(probe.ProbeService, workers=1, args=(probe_inst,))

            for linker_inst in probe_manager.initialize_linkers(graph):
                linker_dispatcher.add_linker(linker_inst)

    def _init_graph(self):
        # TODO: read graph backend from config
        graph_client = graph_drivers.DriverFactory.get('neo4j')
        return Graph(graph_client)
