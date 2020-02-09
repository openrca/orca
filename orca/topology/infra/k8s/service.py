from orca.topology.infra.k8s import extractor


class ServiceExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'service'

    def _extract_properties(self, entity):
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
