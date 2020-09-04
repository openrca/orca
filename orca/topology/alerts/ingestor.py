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

from orca.topology import ingestor


class Ingestor(ingestor.Ingestor):

    """Base class for alert ingestors."""

    def _ingest_event(self, event):
        alert = self._extractor.extract(event)
        if self._graph.get_node(alert.id):
            self._graph.update_node(alert)
            if not alert.is_up:
                self._graph.delete_node(alert.id)
        elif alert.is_up:
            self._graph.add_node(alert)
