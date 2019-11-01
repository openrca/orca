from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import client as k8s_client


class PodProbe(probe.K8SProbe):

    def run(self):
        resource_api = self.client.list_pods_for_all_namespaces
        handler = PodHandler()
        k8s_client.K8SWatch(resource_api, handler).run()


class PodHandler(k8s_client.K8SHandler):

    def on_add(self, obj):
        pass

    def on_update(self, obj):
        pass

    def on_delete(self, obj):
        pass
