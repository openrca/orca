from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher
from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import linker, probe
from orca.topology.probes.k8s import synchronizer as k8s_sync

log = logger.get_logger(__name__)


class SecretProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S sync on resource: secret")
        extractor = SecretExtractor()
        synchronizer = k8s_sync.SynchronizerFactory.get_synchronizer(
            self._graph, self._client, 'secret', extractor)
        synchronizer.synchronize()
        log.info("Finished K8S sync on resource: secret")
        log.info("Starting K8S watch on resource: secret")
        handler = probe.KubeHandler(self._graph, extractor)
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'secret')
        watch.add_handler(handler)
        watch.run()


class SecretExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'secret'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class SecretToPodLinker(linker.Linker):

    @staticmethod
    def create(graph, client):
        fetcher_a = fetcher.GraphFetcher(graph, 'secret')
        fetcher_b = fetcher.GraphFetcher(graph, 'pod')
        matcher = SecretToPodMatcher()
        return SecretToPodLinker(graph, 'secret', fetcher_a, 'pod', fetcher_b, matcher)


class SecretToPodMatcher(linker.Matcher):

    def are_linked(self, secret, pod):
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
