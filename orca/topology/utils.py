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

    def __init__(self, graph):
        self._graph = graph

    def synchronize(self, nodes_in_graph, upstream_nodes, delete=True, update=True, create=True):
        nodes_in_graph = self._build_node_lookup(nodes_in_graph)
        upstream_nodes = self._build_node_lookup(upstream_nodes)

        nodes_in_graph_ids = set(nodes_in_graph.keys())
        upstream_nodes_ids = set(upstream_nodes.keys())

        nodes_to_delete_ids = nodes_in_graph_ids.difference(upstream_nodes_ids)
        nodes_to_update_ids = nodes_in_graph_ids.difference(nodes_to_delete_ids)
        nodes_to_create_ids = upstream_nodes_ids.difference(nodes_in_graph)

        if delete:
            for node_id in nodes_to_delete_ids:
                self._graph.delete_node(nodes_in_graph[node_id])

        if update:
            for node_id in nodes_to_update_ids:
                self._graph.update_node(upstream_nodes[node_id])

        if create:
            for node_id in nodes_to_create_ids:
                self._graph.add_node(upstream_nodes[node_id])

    def _build_node_lookup(self, nodes):
        return {node.id: node for node in nodes}
