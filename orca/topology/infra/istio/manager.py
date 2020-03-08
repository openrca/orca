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

from orca.common.clients.istio import client as istio
from orca.common.clients.k8s import client as k8s
from orca.topology import linker
from orca.topology.infra.istio import destination_rule, gateway, virtual_service
from orca.topology.infra.k8s import probe


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            extractor=virtual_service.VirtualServiceExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'virtual_service')),
        probe.Probe(
            extractor=destination_rule.DestinationRuleExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'destination_rule')),
        probe.Probe(
            extractor=gateway.GatewayExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'gateway'))]


def initialize_linkers(graph):
    return [
        linker.Linker(
            source_kind='virtual_service',
            target_kind='gateway',
            graph=graph,
            matcher=virtual_service.VirtualServiceToGatewayMatcher()),
        linker.Linker(
            source_kind='virtual_service',
            target_kind='service',
            graph=graph,
            matcher=virtual_service.VirtualServiceToServiceMatcher()),
        linker.Linker(
            source_kind='destination_rule',
            target_kind='service',
            graph=graph,
            matcher=destination_rule.DestinationRuleToServiceMatcher())]
