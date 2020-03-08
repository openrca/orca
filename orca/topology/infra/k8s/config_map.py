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
from orca.topology.infra.k8s import linker as k8s_linker


class ConfigMapExtractor(extractor.Extractor):

    def get_kind(self):
        return 'config_map'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class ConfigMapToPodMatcher(linker.Matcher):

    def are_linked(self, config_map, pod):
        match_namespace = k8s_linker.match_namespace(config_map, pod)
        match_env = self._match_env(config_map, pod)
        match_volume = self._match_volume(config_map, pod)
        return match_namespace and (match_env or match_volume)

    def _match_env(self, config_map, pod):
        for container in pod.properties.containers:
            if container.env:
                for env_var in container.env:
                    if env_var.value_from and \
                       env_var.value_from.config_map_key_ref and \
                       env_var.value_from.config_map_key_ref.name == config_map.properties.name:
                        return True
            if container.env_from:
                for env_from in container.env_from:
                    if env_from.config_map_ref and \
                       env_from.config_map_ref.name == config_map.properties.name:
                        return True
        return False

    def _match_volume(self, config_map, pod):
        for volume in pod.properties.volumes:
            if volume.config_map and volume.config_map.name == config_map.properties.name:
                return True
        return False
