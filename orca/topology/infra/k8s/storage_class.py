from orca.topology.infra.k8s import extractor


class StorageClassExtractor(extractor.Extractor):

    def get_kind(self):
        return 'storage_class'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['provisioner'] = entity.provisioner
        properties['reclaim_policy'] = entity.reclaim_policy
        properties['parameters'] = entity.parameters.copy()
        return properties
