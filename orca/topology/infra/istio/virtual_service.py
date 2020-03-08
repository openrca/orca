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

from orca.topology import linker
from orca.topology.infra.istio import extractor
from orca.topology.infra.istio import linker as istio_linker


class VirtualServiceExtractor(extractor.Extractor):

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


class VirtualServiceToGatewayMatcher(linker.Matcher):

    def are_linked(self, virtual_service, gateway):
        return self._match_gateway(virtual_service, gateway)

    def _match_gateway(self, virtual_service, gateway):
        return gateway.properties.name in virtual_service.properties.gateways


class VirtualServiceToServiceMatcher(linker.Matcher):

    def are_linked(self, virtual_service, service):
        namespace = virtual_service.properties.namespace
        if self._match_route_destination(
           namespace, virtual_service.properties.http, service):
            return True
        if self._match_route_destination(
           namespace, virtual_service.properties.tls, service):
            return True
        if self._match_route_destination(
           namespace, virtual_service.properties.tcp, service):
            return True
        return False

    def _match_route_destination(self, namespace, routes, service):
        for route in routes:
            for route_dest in route.route:
                if istio_linker.match_host_to_service(
                   namespace, route_dest.destination.host, service):
                    return True
        return False
