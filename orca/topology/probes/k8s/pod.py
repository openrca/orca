from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.common import logger

log = logger.get_logger(__name__)


class PodProbe(probe.K8SProbe):

    def run(self):
        resource_api = self._client.list_pod_for_all_namespaces
        handler = PodHandler(self._graph)
        log.info("Starting K8S watch on resource: pod")
        k8s_client.Watch(resource_api, handler).run()


class PodHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        properties['ip'] = obj.status.pod_ip
        return (id, properties)


class PodToServiceLinker(linker.K8SLinker):

    @staticmethod
    def create(graph, k8s_client):
        resource_a_api = linker.K8SResourceAPI(
            k8s_client.read_namespaced_pod,
            k8s_client.list_pod_for_all_namespaces
        )
        resource_b_api = linker.K8SResourceAPI(
            k8s_client.read_namespaced_service,
            k8s_client.list_service_for_all_namespaces
        )
        return PodToServiceLinker(
            graph, resource_a_api, resource_b_api)

    def _are_linked(self, pod, service):
        return True
