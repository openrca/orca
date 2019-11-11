from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.common import logger

log = logger.get_logger(__name__)


class ServiceProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: service")
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'service')
        watch.add_handler(ServiceHandler(self._graph))
        watch.run()


class ServiceHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        properties['type'] = obj.spec.type
        properties['ip'] = obj.spec.cluster_ip
        return (id, properties)
