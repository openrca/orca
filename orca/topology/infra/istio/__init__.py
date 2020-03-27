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

from orca.topology.infra.istio import linker, probe
from orca.topology import bundle


def get_probes():
    return [
        bundle.ProbeBundle(
            probe=probe.VirtualServicePullProbe,
            linkers=[
                linker.VirtualServiceToGatewayLinker,
                linker.VirtualServiceToServiceLinker
            ]
        ),

        bundle.ProbeBundle(
            probe=probe.VirtualServicePushProbe,
            linkers=[
                linker.VirtualServiceToGatewayLinker,
                linker.VirtualServiceToServiceLinker
            ]
        ),

        bundle.ProbeBundle(
            probe=probe.DestinationRulePullProbe,
            linkers=[
                linker.DestinationRuleToServiceLinker
            ]
        ),

        bundle.ProbeBundle(
            probe=probe.DestinationRulePushProbe,
            linkers=[
                linker.DestinationRuleToServiceLinker
            ]
        ),

        bundle.ProbeBundle(
            probe=probe.GatewayPullProbe,
            linkers=[
                linker.VirtualServiceToGatewayLinker
            ]
        ),

        bundle.ProbeBundle(
            probe=probe.GatewayPushProbe,
            linkers=[
                linker.VirtualServiceToGatewayLinker
            ]
        ),
    ]
