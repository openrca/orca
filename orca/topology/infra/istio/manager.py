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
from orca.topology import synchronizer
from orca.topology.infra.istio import extractor, linker, probe


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            graph=graph,
            extractor=extractor.VirtualServiceExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'virtual_service')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.DestinationRuleExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'destination_rule')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.GatewayExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'gateway')
        )
    ]


def initialize_linkers(graph):
    return [
        linker.Linker(
            source_kind='virtual_service',
            target_kind='gateway',
            graph=graph,
            matcher=linker.VirtualServiceToGatewayMatcher()
        ),
        linker.Linker(
            source_kind='virtual_service',
            target_kind='service',
            graph=graph,
            matcher=linker.VirtualServiceToServiceMatcher()
        ),
        linker.Linker(
            source_kind='destination_rule',
            target_kind='service',
            graph=graph,
            matcher=linker.DestinationRuleToServiceMatcher()
        )
    ]
