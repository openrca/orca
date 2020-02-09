from orca.topology.infra.k8s import extractor


class DeploymentExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'deployment'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['selector'] = entity.spec.selector.match_labels
        return properties
