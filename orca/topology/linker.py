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

import abc
from collections import defaultdict

from orca.graph import graph


class EventDispatcher(graph.EventListener):

    """Listens for graph events and triggers node linking on node updates."""

    def __init__(self):
        self._linkers = defaultdict(lambda: defaultdict(list))

    def add_linker(self, linker):
        self._build_lookup(linker.source_spec, linker)
        if linker.bidirectional:
            self._build_lookup(linker.target_spec, linker)

    def on_node_added(self, node):
        self._link_node(node)

    def on_node_updated(self, node):
        self._link_node(node)

    def on_node_deleted(self, node):
        return

    def on_link_added(self, link):
        return

    def on_link_updated(self, link):
        return

    def on_link_deleted(self, link):
        return

    def _build_lookup(self, node_spec, linker):
        self._linkers[node_spec.origin][node_spec.kind].append(linker)

    def _link_node(self, node):
        for linker in self._linkers[node.origin][node.kind]:
            linker.link(node)


class Linker(abc.ABC):

    """Links pairs of nodes based on the matching condition."""

    def __init__(self, graph, source_spec, target_spec, matcher, bidirectional=True):
        super().__init__()
        self.source_spec = source_spec
        self.target_spec = target_spec
        self.bidirectional = bidirectional
        self._graph = graph
        self._matcher = matcher

    def link(self, node):
        with self._graph.locked():
            self._link_node(node)

    def _link_node(self, node):
        current_links = self._build_link_lookup(self._get_current_links(node))
        new_links = self._build_link_lookup(self._get_new_links(node))

        current_links_ids = set(current_links.keys())
        new_links_ids = set(new_links.keys())

        links_to_delete_ids = current_links_ids.difference(new_links_ids)
        links_to_update_ids = current_links_ids.difference(links_to_delete_ids)
        links_to_create_ids = new_links_ids.difference(current_links_ids)

        for link_id in links_to_delete_ids:
            self._graph.delete_link(link_id)

        for link_id in links_to_update_ids:
            self._graph.update_link(new_links[link_id])

        for link_id in links_to_create_ids:
            self._graph.add_link(new_links[link_id])

    def _get_current_links(self, node):
        target_spec = self._get_target_spec(node)
        return self._graph.get_node_links(
            node, origin=target_spec.origin, kind=target_spec.kind)

    def _get_target_spec(self, node):
        if self._is_source(node):
            return self.target_spec
        return self.source_spec

    def _get_new_links(self, node):
        if self._is_source(node):
            return self._get_links_from_source(node)
        return self._get_links_from_target(node)

    def _is_source(self, node):
        if node.origin == self.source_spec.origin and \
           node.kind == self.source_spec.kind:
            return True
        return False

    def _get_links_from_source(self, source_node):
        links = []
        target_nodes = self._get_target_nodes(source_node)
        for target_node in target_nodes:
            if self._matcher.are_linked(source_node, target_node):
                links.append(graph.Graph.create_link({}, source_node, target_node))
        return links

    def _get_target_nodes(self, source_node):
        return self._get_nodes_by_spec(self.target_spec)

    def _get_links_from_target(self, target_node):
        links = []
        source_nodes = self._get_source_nodes(target_node)
        for source_node in source_nodes:
            if self._matcher.are_linked(source_node, target_node):
                links.append(graph.Graph.create_link({}, source_node, target_node))
        return links

    def _get_source_nodes(self, target_node):
        return self._get_nodes_by_spec(self.source_spec)

    def _get_nodes_by_spec(self, node_spec):
        return self._graph.get_nodes(origin=node_spec.origin, kind=node_spec.kind)

    def _build_link_lookup(self, links):
        return {link.id: link for link in links}
