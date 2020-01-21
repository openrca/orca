from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import synchronizer as k8s_sync

log = logger.get_logger(__name__)


class ServiceProbe(probe.Probe):

    @staticmethod
    def create(graph, client):
        extractor = ServiceExtractor()
        synchronizer = k8s_sync.SynchronizerFactory.get_synchronizer(
            graph, client, 'service', extractor)
        handler = probe.KubeHandler(graph, extractor)
        watcher = k8s_client.ResourceWatch(client.CoreV1Api(), 'service')
        watcher.add_handler(handler)
        return ServiceProbe('service', synchronizer, watcher)


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
