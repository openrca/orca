from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import probe

log = logger.get_logger(__name__)


class ServiceExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['type'] = entity.spec.type
        properties['ip'] = entity.spec.cluster_ip
        return properties


class ServiceProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: service")
        extractor = ServiceExtractor()
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'service')
        watch.add_handler(ServiceHandler(self._graph, extractor))
        watch.run()


class ServiceHandler(probe.K8SResourceHandler):
    pass
