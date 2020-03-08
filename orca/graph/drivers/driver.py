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


class Driver(abc.ABC):

    """Abstract Graph DB driver."""

    @abc.abstractmethod
    def get_nodes(self, kind, properties):
        """Gets all graph nodes."""

    @abc.abstractmethod
    def get_node(self, id, kind, properties):
        """Gets graph node details."""

    @abc.abstractmethod
    def add_node(self, node):
        """Creates a graph node."""

    @abc.abstractmethod
    def update_node(self, node):
        """Updates a graph node."""

    @abc.abstractmethod
    def delete_node(self, node):
        """Deletes a graph node."""

    @abc.abstractmethod
    def get_links(self, properties):
        """Gets all graph links."""

    @abc.abstractmethod
    def get_link(self, id, properties):
        """Gets graph link details."""

    @abc.abstractmethod
    def add_link(self, link):
        """Creates a graph link."""

    @abc.abstractmethod
    def update_link(self, link):
        """Updates a graph link."""

    @abc.abstractmethod
    def delete_link(self, link):
        """Deletes a graph link."""

    @abc.abstractmethod
    def get_node_links(self, node, kind):
        """Gets links connected to a node."""
