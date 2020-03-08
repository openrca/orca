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

from orca.graph import graph
from orca.topology import extractor


class Extractor(extractor.Extractor):

    def get_origin(self):
        return 'kubernetes'

    def extract(self, entity):
        node_id = self._extract_id(entity)
        properties = self._extract_properties(entity)
        return graph.Node(node_id, properties, self.get_origin(), self.get_kind())

    def _extract_id(self, entity):
        return entity.metadata.uid

    @abc.abstractmethod
    def _extract_properties(self, entity):
        """Extracts properties from given K8S object."""
