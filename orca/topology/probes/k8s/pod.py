from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import client as k8s_client
from orca.common import logger

log = logger.get_logger(__name__)


class PodProbe(probe.K8SProbe):

    def run(self):
        resource_api = self._client.list_pods_for_all_namespaces
        handler = PodHandler(self._graph)
        log.info("Starting K8S watch on resource: pod")
        k8s_client.Watch(resource_api, handler).run()


class PodHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        return (123, {})
