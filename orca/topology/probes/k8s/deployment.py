from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher
from orca.topology.probes import synchronizer as sync
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import fetcher as k8s_fetcher
from orca.topology.probes.k8s import probe

log = logger.get_logger(__name__)


class DeploymentProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S sync on resource: deployment")
        extractor = DeploymentExtractor()
        graph_fetcher = fetcher.GraphFetcher(self._graph, 'deployment')
        upstream_fetcher = k8s_fetcher.FetcherFactory.get_fetcher(self._client, 'deployment', extractor)
        synchronizer = sync.Synchronizer(self._graph, graph_fetcher, upstream_fetcher)
        synchronizer.synchronize()
        log.info("Finished K8S sync on resource: deployment")
        log.info("Starting K8S watch on resource: deployment")
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.AppsV1Api(), 'deployment')
        watch.add_handler(handler)
        watch.run()


class DeploymentExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'deployment'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['selector'] = entity.spec.selector.match_labels
        return properties
