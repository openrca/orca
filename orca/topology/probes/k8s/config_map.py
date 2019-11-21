from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.common import logger

log = logger.get_logger(__name__)


class ConfigMapProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: config_map")
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'config_map')
        watch.add_handler(ConfigMapHandler(self._graph))
        watch.run()


class ConfigMapHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        return (id, 'config_map', properties)


class ConfigMapToPodLinker(linker.K8SLinker):

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
        return ConfigMapToPodLinker(
            graph,
            'config_map', k8s_client.ResourceAPI(client.CoreV1Api(), 'config_map'),
            'pod', k8s_client.ResourceAPI(client.CoreV1Api(), 'pod'))
