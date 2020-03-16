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

import copy

from orca.topology.infra.k8s import extractor


class Extractor(extractor.Extractor):

    """Base class for Istio extractors."""

    def get_origin(self):
        return 'istio'


class VirtualServiceExtractor(Extractor):

    """Extractor for Virtual Service entities."""

    def get_kind(self):
        return 'virtual_service'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['gateways'] = entity.spec.gateways.copy()
        properties['hosts'] = entity.spec.hosts.copy()
        properties['http'] = copy.deepcopy(entity.spec.http) if entity.spec.http else []
        properties['tls'] = copy.deepcopy(entity.spec.tls) if entity.spec.tls else []
        properties['tcp'] = copy.deepcopy(entity.spec.tcp) if entity.spec.tcp else []
        return properties


class DestinationRuleExtractor(Extractor):

    """Extractor for Destination Rule entities."""

    def get_kind(self):
        return 'destination_rule'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['host'] = entity.spec.host
        return properties


class GatewayExtractor(Extractor):

    """Extractor for Gateway entities."""

    def get_kind(self):
        return 'gateway'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties
