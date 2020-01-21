from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher
from orca.topology.probes.k8s import extractor, linker, probe

log = logger.get_logger(__name__)


class ConfigMapProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: config_map")
        extractor = ConfigMapExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'config_map')
        watch.add_handler(handler)
        watch.run()


class ConfigMapExtractor(extractor.Extractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class ConfigMapToPodLinker(linker.Linker):

    @staticmethod
    def create(graph, client):
        fetcher_a = fetcher.GraphFetcher(graph, 'configmap')
        fetcher_b = fetcher.GraphFetcher(graph, 'pod')
        matcher = ConfigMapToPodMatcher()
        return ConfigMapToPodLinker(
            graph, 'configmap', fetcher_a, 'pod', fetcher_b, matcher)


class ConfigMapToPodMatcher(linker.Matcher):

    def are_linked(self, config_map, pod):
        match_namespace = self._match_namespace(config_map, pod)
        match_env = self._match_env(config_map, pod)
        match_volume = self._match_volume(config_map, pod)
        return match_namespace and (match_env or match_volume)

    def _match_env(self, config_map, pod):
        for container in pod.properties.containers:
            if container.env:
                for env_var in container.env:
                    if env_var.value_from and \
                       env_var.value_from.config_map_key_ref and \
                       env_var.value_from.config_map_key_ref.name == config_map.properties.name:
                        return True
            if container.env_from:
                for env_from in container.env_from:
                    if env_from.config_map_ref and \
                       env_from.config_map_ref.name == config_map.properties.name:
                        return True
        return False

    def _match_volume(self, config_map, pod):
        for volume in pod.properties.volumes:
            if volume.config_map and volume.config_map.name == config_map.properties.name:
                return True
        return False
