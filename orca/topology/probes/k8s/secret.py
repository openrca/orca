from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.common import logger

log = logger.get_logger(__name__)


class SecretProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: secret")
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'secret')
        watch.add_handler(SecretHandler(self._graph))
        watch.run()


class SecretHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        return (id, 'secret', properties)


class SecretToPodLinker(linker.K8SLinker):

    def _are_linked(self, secret, pod):
        match_namespace = self._match_namespace(secret, pod)
        match_volume = self._match_volume(secret, pod)
        return match_namespace and match_volume

    def _match_volume(self, secret, pod):
        for volume in pod.spec.volumes:
            if volume.secret and volume.secret.secret_name == secret.metadata.name:
                return True
        return False

    @staticmethod
    def create(graph, client):
        return SecretToPodLinker(
            graph,
            'secret', k8s_client.ResourceAPI(client.CoreV1Api(), 'secret'),
            'pod', k8s_client.ResourceAPI(client.CoreV1Api(), 'pod'))
