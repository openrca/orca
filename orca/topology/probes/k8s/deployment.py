from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import probe

log = logger.get_logger(__name__)


class DeploymentExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class DeploymentProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: deployment")
        extractor = DeploymentExtractor()
        watch = k8s_client.ResourceWatch(self._client.AppsV1Api(), 'deployment')
        watch.add_handler(DeploymentHandler(self._graph, extractor))
        watch.run()


class DeploymentHandler(probe.K8SResourceHandler):
    pass
