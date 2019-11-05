from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import client as k8s_client
from orca.common import logger

log = logger.get_logger(__name__)


class DeploymentProbe(probe.K8SProbe):

    def run(self):
        resource_api = self._client.list_pod_for_all_namespaces
        handler = DeploymentHandler(self._graph)
        log.info("Starting K8S watch on resource: deployment")
        k8s_client.Watch(resource_api, handler).run()


class DeploymentHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        return (id, properties)
