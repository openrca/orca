import cotyledon

from orca.graph import drivers as graph_drivers
from orca.graph.graph import Graph
from orca.common.clients import k8s
from orca.topology import linker, probe
from orca.topology.alerts.elastalert import alert as prom_alert
from orca.topology.alerts.falco import alert as falco_alert
from orca.topology.alerts.prometheus import alert as es_alert
from orca.topology.infra import k8s as k8s_probe
from orca.topology.infra import istio as istio_probe


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()
        graph = self._init_graph()
        self._add_k8s_probes(graph)
        self._add_alert_probes(graph)

    def _init_graph(self):
        # TODO: read graph backend from config
        graph_client = graph_drivers.DriverFactory.get('neo4j')
        return Graph(graph_client)

    def _add_k8s_probes(self, graph):
        k8s_client = k8s.ClientFactory.get()

        linker_dispatcher = linker.Dispatcher()
        for k8s_linker in k8s_probe.LINKERS:
            linker_dispatcher.add_linker(k8s_linker.create(graph))

        graph.add_listener(linker_dispatcher)

        for probe_klass in k8s_probe.PROBES:
            probe_inst = probe_klass.create(graph, k8s_client)
            self.add(probe.ProbeService, workers=1, args=(probe_inst,))

        for probe_klass in istio_probe.PROBES:
            probe_inst = probe_klass.create(graph, k8s_client)
            self.add(probe.ProbeService, workers=1, args=(probe_inst,))

    def _add_alert_probes(self, graph):
        prom_probe = prom_alert.AlertProbe.create(graph)
        falco_probe = falco_alert.AlertProbe.create(graph)
        es_probe = es_alert.AlertProbe.create(graph)

        self.add(probe.ProbeService, workers=1, args=(prom_probe,))
        self.add(probe.ProbeService, workers=1, args=(falco_probe,))
        self.add(probe.ProbeService, workers=1, args=(es_probe,))
