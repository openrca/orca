
from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.common import logger

log = logger.get_logger(__name__)


class NodeProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: node")
        watch = k8s_client.ResourceWatch(
            self._client.CoreV1Api(), 'node', namespaced=False)
        watch.add_handler(NodeHandler(self._graph))
        watch.run()


class NodeHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        return (id, 'node', properties)
