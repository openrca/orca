# Copyright 2020 OpenRCA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from orca.topology import linker
from orca.topology.infra.k8s import extractor


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


class PersistentVolumeToPersistentVolumeClaimMatcher(linker.Matcher):

    def are_linked(self, pv, pvc):
        return pv.properties.name == pvc.properties.volume_name
