from orca.topology.infra.k8s import extractor


class DeploymentExtractor(extractor.Extractor):

    def get_kind(self):
        return 'deployment'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['selector'] = entity.spec.selector.match_labels
        return properties
