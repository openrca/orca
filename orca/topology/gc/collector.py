# Copyright 2021 OpenRCA Authors
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

import abc
import time

from orca.common import utils


class Collector(abc.ABC):

    """Base class for garbage collectors."""

    def __init__(self, graph):
        self._graph = graph

    @abc.abstractmethod
    def collect(self):
        """Collects graph nodes for removal."""


class StaleNodeCollector(Collector):

    """Collects graph nodes based on staleness period."""

    def __init__(self, graph, node_spec, staleness_period=300):
        super().__init__(graph)
        self._node_spec = node_spec
        self._staleness_period = staleness_period

    def collect(self):
        nodes = self._graph.get_nodes(
            properties={'origin': self._node_spec.origin, 'kind': self._node_spec.kind})
        nodes_to_remove = []
        for node in nodes:
            if utils.get_utc() - node.updated_at > self._staleness_period:
                nodes_to_remove.append(node)
        return nodes_to_remove
