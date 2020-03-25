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
from orca.topology import utils
from orca.topology.infra.istio import linker, probe, matcher

CONFIG = config.CONFIG


def initialize_probes(graph):
    return [
        probe.VirtualServicePullProbe.get(graph),
        probe.VirtualServicePushProbe.get(graph),
        probe.DestinationRulePullProbe.get(graph),
        probe.DestinationRulePushProbe.get(graph),
        probe.GatewayPullProbe.get(graph),
        probe.GatewayPushProbe.get(graph)
    ]


def initialize_linkers(graph):
    return [
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='virtual_service'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='gateway'),
            matcher=matcher.VirtualServiceToGatewayMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='virtual_service'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=matcher.VirtualServiceToServiceMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='destination_rule'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=matcher.DestinationRuleToServiceMatcher()
        )
    ]
