from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import probe
from orca.topology.probes.k8s import synchronizer as k8s_sync

log = logger.get_logger(__name__)


class DeploymentProbe(probe.Probe):

    @staticmethod
    def create(graph, client):
        extractor = DeploymentExtractor()
        synchronizer = k8s_sync.SynchronizerFactory.get_synchronizer(
            graph, client, 'deployment', extractor)
        handler = probe.KubeHandler(graph, extractor)
        watcher = k8s_client.ResourceWatch(client.AppsV1Api(), 'deployment')
        watcher.add_handler(handler)
        return DeploymentProbe('deployment', synchronizer, watcher)


class DeploymentExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'deployment'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['selector'] = entity.spec.selector.match_labels
        return properties
