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

from orca import exceptions
from orca.common import logger

LOG = logger.get_logger(__name__)


class Ingestor(object):

    """Processes entity events received from the upstream."""

    def __init__(self, graph, extractor):
        self._graph = graph
        self._extractor = extractor

    def ingest(self, event):
        LOG.debug("Ingested event: %s", event)
        try:
            self._ingest_event(event)
        except exceptions.OrcaError as ex:
            LOG.warning("Error while extracting an entity: %s", ex)

    def _ingest_event(self, event):
        node = self._extractor.extract(event)
        if self._graph.get_node(node.id):
            self._graph.update_node(node)
        else:
            self._graph.add_node(node)
