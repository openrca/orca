from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import graph as graph_fetcher
from orca.topology.probes.k8s import extractor, linker, probe

log = logger.get_logger(__name__)


class ConfigMapExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class ConfigMapProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: config_map")
        extractor = ConfigMapExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'config_map')
        watch.add_handler(handler)
        watch.run()


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


class ConfigMapToPodLinker(linker.Linker):

    @staticmethod
    def create(graph, client):
        config_map_fetcher = graph_fetcher.Fetcher(graph, 'configmap')
        pod_fetcher = graph_fetcher.Fetcher(graph, 'pod')
        matcher = ConfigMapToPodMatcher()
        return ConfigMapToPodLinker(
            graph, 'configmap', config_map_fetcher, 'pod', pod_fetcher, matcher)
