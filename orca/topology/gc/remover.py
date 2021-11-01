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

class Remover:

    """Removes collected graph nodes."""

    def __init__(self, graph, collectors):
        self._graph = graph
        self._collectors = collectors

    def run(self):
        nodes_to_remove = []
        with self._graph.locked():
            for collector in self._collectors:
                nodes_to_remove.extend(collector.collect())
            for node in nodes_to_remove:
                self._graph.delete_node(node.id)
        return nodes_to_remove

