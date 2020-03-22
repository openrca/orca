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

from orca.common import config
from orca.common.clients.istio import client as istio
from orca.common.clients.k8s import client as k8s
from orca.topology import probe, utils
from orca.topology.infra.istio import extractor, linker
from orca.topology.infra.k8s import upstream

CONFIG = config.CONFIG


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.PullProbe(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get(k8s_client, 'virtual_service')),
            extractor=extractor.VirtualServiceExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.istio.resync_period
        ),
        probe.PullProbe(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get(k8s_client, 'destination_rule')),
            extractor=extractor.DestinationRuleExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.istio.resync_period
        ),
        probe.PullProbe(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get(k8s_client, 'gateway')),
            extractor=extractor.GatewayExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.istio.resync_period
        ),

        probe.PushProbe(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get(k8s_client, 'virtual_service')),
            extractor=extractor.VirtualServiceExtractor()
        ),
        probe.PushProbe(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get(k8s_client, 'destination_rule')),
            extractor=extractor.DestinationRuleExtractor()
        ),
        probe.PushProbe(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get(k8s_client, 'gateway')),
            extractor=extractor.GatewayExtractor()
        )
    ]


def initialize_linkers(graph):
    return [
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='virtual_service'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='gateway'),
            matcher=linker.VirtualServiceToGatewayMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='virtual_service'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=linker.VirtualServiceToServiceMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='destination_rule'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=linker.DestinationRuleToServiceMatcher()
        )
    ]
