from orca.k8s import client as k8s
from orca.topology.infra.k8s import extractor, probe


class ServiceProbe(probe.Probe):

    @staticmethod
    def create(graph, k8s_client):
        return ServiceProbe('service', ServiceExtractor(), graph,
                            k8s.ResourceProxy.get(k8s_client, 'service'))


class ServiceExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'service'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['type'] = entity.spec.type
        properties['ip'] = entity.spec.cluster_ip
        if entity.spec.selector:
            properties['selector'] = entity.spec.selector.copy()
        else:
            properties['selector'] = {}
        return properties
