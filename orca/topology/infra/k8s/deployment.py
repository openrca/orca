from orca.k8s import client as k8s
from orca.topology.infra.k8s import extractor, probe


class DeploymentProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return DeploymentProbe('deployment', DeploymentExtractor(), graph,
                               k8s.ResourceProxy.get(k8s_client, 'deployment'))


class DeploymentExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'deployment'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['selector'] = entity.spec.selector.match_labels
        return properties
