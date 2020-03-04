from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class PersistentVolumeClaimExtractor(extractor.Extractor):

    def get_kind(self):
        return 'persistent_volume_claim'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['storage_class'] = entity.spec.storage_class_name
        properties['volume_name'] = entity.spec.volume_name
        return properties
