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

from orca.topology import utils
from orca.topology import linker
from orca.topology.infra.istio import matcher


class Linker(linker.Linker):

    """Base class for Istio linkers."""


class VirtualServiceToGatewayLinker(Linker):

    """Links Virtual Service entities to Gateway entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='istio', kind='virtual_service'),
            target_spec=utils.NodeSpec(origin='istio', kind='gateway'),
            matcher=matcher.VirtualServiceToGatewayMatcher())


class VirtualServiceToServiceLinker(Linker):

    """Links Virtual Service entities to Service entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='istio', kind='virtual_service'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=matcher.VirtualServiceToServiceMatcher())


class DestinationRuleToServiceLinker(Linker):

    """Links Destination Rule entities to Service entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='istio', kind='destination_rule'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=matcher.DestinationRuleToServiceMatcher())
