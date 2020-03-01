from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class PersistentVolumeExtractor(extractor.Extractor):

    def get_kind(self):
        return 'persistent_volume'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['storage_class'] = entity.spec.storage_class_name
        if entity.spec.nfs:
            properties['nfs'] = self._extract_nfs(entity.spec.nfs)
        properties['host_path'] = entity.spec.host_path
        properties['capacity'] = None
        if entity.spec.capacity:
            properties['capacity'] = entity.spec.capacity.copy()
        return properties

    def _extract_nfs(self, nfs):
        nfs_properties = {}
        nfs_properties['path'] = nfs.path
        nfs_properties['read_only'] = nfs.read_only
        nfs_properties['server'] = nfs.server
        return nfs_properties


class PersistentVolumeToStorageClassMatcher(linker.Matcher):

    def are_linked(self, persistent_volume, storage_class):
        if persistent_volume.properties.storage_class and \
           persistent_volume.properties.storage_class == storage_class.properties.name:
            return True
        return False
