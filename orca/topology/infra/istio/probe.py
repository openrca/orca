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
from orca.topology import probe, utils
from orca.topology.infra.istio import extractor
from orca.topology.infra.k8s import upstream

CONFIG = config.CONFIG


class VirtualServicePullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get('virtual_service')),
            extractor=extractor.VirtualServiceExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class DestinationRulePullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get('destination_rule')),
            extractor=extractor.DestinationRuleExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class GatewayPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get('gateway')),
            extractor=extractor.GatewayExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class VirtualServicePushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get('virtual_service')),
            extractor=extractor.VirtualServiceExtractor())


class DestinationRulePushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get('destination_rule')),
            extractor=extractor.DestinationRuleExtractor())


class GatewayPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=istio.ResourceProxyFactory.get('gateway')),
            extractor=extractor.GatewayExtractor())
