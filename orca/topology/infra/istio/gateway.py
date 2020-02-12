from orca.topology.infra.k8s import extractor


class GatewayExtractor(extractor.Extractor):

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties
