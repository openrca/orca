import cotyledon

from orca.topology.probes import k8s
from orca.topology.probes.k8s import client as k8s_client


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()
        self._add_k8s_probes()

    def _add_k8s_probes(self):
        client = k8s_client.ClientFactory.get_client()
        for probe in k8s.PROBES:
            self.add(probe, workers=1, args=(client))
