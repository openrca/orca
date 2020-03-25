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


class PullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph, kind, extractor):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(istio.ResourceProxyFactory.get(kind)),
            extractor=extractor,
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.istio.resync_period)


class PushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph, kind, extractor):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(istio.ResourceProxyFactory.get(kind)),
            extractor=extractor)


class VirtualServicePullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'virtual_service', extractor.VirtualServiceExtractor())


class DestinationRulePullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'destination_rule', extractor.DestinationRuleExtractor())


class GatewayPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'gateway', extractor.GatewayExtractor())


class VirtualServicePushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'virtual_service', extractor.VirtualServiceExtractor())


class DestinationRulePushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'destination_rule', extractor.DestinationRuleExtractor())


class GatewayPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'gateway', extractor.GatewayExtractor())
