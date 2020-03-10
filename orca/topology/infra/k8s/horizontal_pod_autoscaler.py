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


class HorizontalPodAutoscalerExtractor(extractor.Extractor):

    def get_kind(self):
        return 'horizontal_pod_autoscaler'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['min_replicas'] = entity.spec.min_replicas
        properties['max_replicas'] = entity.spec.max_replicas
        properties['target_ref'] = self._extract_target_ref(entity.spec.scale_target_ref)
        return properties

    def _extract_target_ref(self, target_ref):
        return {'kind': target_ref.kind.lower(), 'name': target_ref.name}


class HorizontalPodAutoscalerMatcher(linker.Matcher):

    def are_linked(self, obj, hpa):
        match_namespace = k8s_linker.match_namespace(obj, hpa)
        match_target_ref = self._match_target_ref(obj, hpa)
        return match_namespace and match_target_ref

    def _match_target_ref(self, obj, hpa):
        return hpa.properties.target_ref.kind == obj.kind and \
               hpa.properties.target_ref.name == obj.properties.name
