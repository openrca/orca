from orca.topology.infra.istio import extractor


class GatewayExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'gateway'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties
