from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import indexer as k8s_indexer
from orca.topology.probes.k8s import linker, probe

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
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'config_map')
        watch.add_handler(ConfigMapHandler(self._graph, extractor))
        watch.run()


class ConfigMapHandler(probe.K8SResourceHandler):
    pass


class ConfigMapToPodLinker(linker.Linker):

    def _are_linked(self, config_map, pod):
        match_namespace = self._match_namespace(config_map, pod)
        match_env = self._match_env(config_map, pod)
        match_volume = self._match_volume(config_map, pod)
        return match_namespace and (match_env or match_volume)

    def _match_env(self, config_map, pod):
        for container in pod.spec.containers:
            if container.env:
                for env_var in container.env:
                    if env_var.value_from and \
                       env_var.value_from.config_map_key_ref and \
                       env_var.value_from.config_map_key_ref.name == config_map.metadata.name:
                        return True
            if container.env_from:
                for env_from in container.env_from:
                    if env_from.config_map_ref and \
                       env_from.config_map_ref.name == config_map.metadata.name:
                        return True
        return False

    def _match_volume(self, config_map, pod):
        for volume in pod.spec.volumes:
            if volume.config_map and volume.config_map.name == config_map.metadata.name:
                return True
        return False

    @staticmethod
    def create(graph, client):
        config_map_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'config_map')
        pod_indexer = k8s_indexer.IndexerFactory.get_indexer(client, 'pod')
        return ConfigMapToPodLinker(graph, 'config_map', config_map_indexer, 'pod', pod_indexer, )
