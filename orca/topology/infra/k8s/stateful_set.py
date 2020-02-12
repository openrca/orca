from orca.topology.infra.k8s import extractor


class StatefulSetExtractor(extractor.Extractor):

    def get_kind(self):
        return 'steteful_set'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties
