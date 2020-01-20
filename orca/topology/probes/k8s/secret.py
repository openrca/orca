from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import graph as graph_indexer
from orca.topology.probes.k8s import extractor, linker, probe

log = logger.get_logger(__name__)


class SecretExtractor(extractor.KubeExtractor):

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class SecretProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: secret")
        extractor = SecretExtractor()
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'secret')
        watch.add_handler(handler)
        watch.run()


class SecretToPodLinker(linker.Linker):

    def _are_linked(self, secret, pod):
        match_namespace = self._match_namespace(secret, pod)
        match_env = self._match_env(secret, pod)
        match_volume = self._match_volume(secret, pod)
        return match_namespace and (match_env or match_volume)

    def _match_env(self, secret, pod):
        for container in pod.properties.containers:
            if container.env:
                for env_var in container.env:
                    if env_var.value_from and \
                       env_var.value_from.secret_key_ref and \
                       env_var.value_from.secret_key_ref.name == secret.properties.name:
                        return True
            if container.env_from:
                for env_from in container.env_from:
                    if env_from.secret_ref and \
                       env_from.secret_ref.name == secret.properties.name:
                        return True
        return False

    def _match_volume(self, secret, pod):
        for volume in pod.properties.volumes:
            if volume.secret and volume.secret.secret_name == secret.properties.name:
                return True
        return False

    @staticmethod
    def create(graph, client):
        secret_indexer = graph_indexer.Indexer(graph, 'secret')
        pod_indexer = graph_indexer.Indexer(graph, 'pod')
        return SecretToPodLinker(graph, 'secret', secret_indexer, 'pod', pod_indexer)
