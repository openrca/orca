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


class NodeSynchronizer(object):

    """Synchronizes given set of nodes into the graph."""

    def __init__(self, graph):
        self._graph = graph

    def synchronize(self, current_nodes, new_nodes, delete=True, update=True, create=True):
        current_nodes = self._build_node_lookup(current_nodes)
        new_nodes = self._build_node_lookup(new_nodes)

        current_nodes_ids = set(current_nodes.keys())
        new_nodes_ids = set(new_nodes.keys())

        nodes_to_delete_ids = current_nodes_ids.difference(new_nodes_ids)
        nodes_to_update_ids = current_nodes_ids.difference(nodes_to_delete_ids)
        nodes_to_create_ids = new_nodes_ids.difference(current_nodes)

        if delete:
            for node_id in nodes_to_delete_ids:
                self._graph.delete_node(current_nodes[node_id])

        if update:
            for node_id in nodes_to_update_ids:
                self._graph.update_node(new_nodes[node_id])

        if create:
            for node_id in nodes_to_create_ids:
                self._graph.add_node(new_nodes[node_id])

    def _build_node_lookup(self, nodes):
        return {node.id: node for node in nodes}


class NodeSpec(object):

    """Value object containing basic node properties."""

    def __init__(self, origin, kind, properties=None):
        self.origin = origin
        self.kind = kind
        self.properties = properties
