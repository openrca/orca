from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import probe

log = logger.get_logger(__name__)


class ServiceProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: service")
        extractor = ServiceExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'service')
        watch.add_handler(handler)
        watch.run()


class ServiceExtractor(extractor.Extractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['type'] = entity.spec.type
        properties['ip'] = entity.spec.cluster_ip
        if entity.spec.selector:
            properties['selector'] = entity.spec.selector.copy()
        else:
            properties['selector'] = {}
        return properties
