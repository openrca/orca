from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import synchronizer as k8s_sync

log = logger.get_logger(__name__)


class ServiceProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S sync on resource: service")
        extractor = ServiceExtractor()
        synchronizer = k8s_sync.SynchronizerFactory.get_synchronizer(
            self._graph, self._client, 'service', extractor)
        synchronizer.synchronize()
        log.info("Finished K8S sync on resource: service")
        log.info("Starting K8S watch on resource: service")
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'service')
        watch.add_handler(handler)
        watch.run()


class ServiceExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'service'

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
