from orca.topology.probes import probe


class K8SProbe(probe.Probe):

    def __init__(self, probe_id, client):
        super().__init__(probe_id)
        self._client = client
