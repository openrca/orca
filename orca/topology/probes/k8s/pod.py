from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import client as k8s_client
from orca.graph import client as graph_client


class PodProbe(probe.K8SProbe):

    def run(self):
        resource_api = self._client.list_pods_for_all_namespaces
        handler = PodHandler(self._graph)
        k8s_client.Watch(resource_api, handler).run()


class PodHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        return (123, {})
