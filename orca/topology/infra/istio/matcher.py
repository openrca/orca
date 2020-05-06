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

from orca.topology import matcher


class Matcher(matcher.Matcher):

    """Base class for Istio matchers."""


class GatewayToVirtualServiceMatcher(Matcher):

    """Matcher for links between Gateway and Virtual Service entities."""

    def are_linked(self, gateway, virtual_service):
        return self._match_gateway(virtual_service, gateway)

    def _match_gateway(self, virtual_service, gateway):
        return gateway.properties.name in virtual_service.properties.gateways


class ServiceToVirtualServiceMatcher(Matcher):

    """Matcher for links between Service and Virtual Service entities."""

    def are_linked(self, service, virtual_service):
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
                if match_host_to_service(
                   namespace, route_dest.destination.host, service):
                    return True
        return False


class ServiceToDestinationRuleMatcher(Matcher):

    """Matcher for links between Service and Destination Rule entities."""

    def are_linked(self, service, destination_rule):
        return match_host_to_service(
            destination_rule.properties.namespace, destination_rule.properties.host, service)


def match_host_to_service(namespace, host, service):
    host_parts = host.split('.')
    service_name = host_parts[0]
    service_namespace = host_parts[1] if len(host_parts) > 1 else namespace
    matched_name = service_name == service.properties.name
    matched_namespace = service_namespace == service.properties.namespace
    return matched_name and matched_namespace
