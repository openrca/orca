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


class PersistentVolumeClaimToPodMatcher(linker.Matcher):

    def are_linked(self, pvc, pod):
        match_namespace = k8s_linker.match_namespace(pvc, pod)
        match_volume = self._match_volume(pvc, pod)
        return match_namespace and match_volume

    def _match_volume(self, pvc, pod):
        for volume in pod.properties.volumes:
            if volume.persistent_volume_claim and \
               volume.persistent_volume_claim.claim_name == pvc.properties.name:
                return True
        return False

