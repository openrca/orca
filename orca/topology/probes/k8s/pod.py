from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.common import logger

log = logger.get_logger(__name__)


class PodProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: pod")
        watch = k8s_client.ResourceWatch(self._client.CoreV1Api(), 'pod')
        watch.add_handler(PodHandler(self._graph))
        watch.run()


class PodHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        properties['ip'] = obj.status.pod_ip
        return (id, 'pod', properties)


class PodToServiceLinker(linker.K8SLinker):

    def _are_linked(self, pod, service):
        match_namespace = self._match_namespace(pod, service)
        match_selector = self._match_selector(pod, service.spec.selector)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        return PodToServiceLinker(
            graph,
            k8s_client.ResourceAPI(client.CoreV1Api(), 'pod'),
            k8s_client.ResourceAPI(client.CoreV1Api(), 'service'))


class PodToDeploymentLinker(linker.K8SLinker):

    def _are_linked(self, pod, deployment):
        match_namespace = self._match_namespace(pod, deployment)
        match_selector = self._match_selector(pod, deployment.spec.selector.match_labels)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        return PodToDeploymentLinker(
            graph,
            k8s_client.ResourceAPI(client.CoreV1Api(), 'pod'),
            k8s_client.ResourceAPI(client.AppsV1Api(), 'deployment'))
