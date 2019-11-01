from orca.topology.probes import probe
from orca.topology.probes.k8s import client as k8s_client


class K8SProbe(probe.Probe):

    def __init__(self, probe_id):
        super().__init__(probe_id)
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = k8s_client.K8SClientFactory.get_client()
        return self._client
