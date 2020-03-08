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
from orca.topology.infra.istio import extractor
from orca.topology.infra.istio import linker as istio_linker


class DestinationRuleExtractor(extractor.Extractor):

    def get_kind(self):
        return 'destination_rule'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['host'] = entity.spec.host
        return properties


class DestinationRuleToServiceMatcher(linker.Matcher):

    def are_linked(self, destination_rule, service):
        return istio_linker.match_host_to_service(
            destination_rule.properties.namespace, destination_rule.properties.host, service)
