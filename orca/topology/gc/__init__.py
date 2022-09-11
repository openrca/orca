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

import time

import cotyledon

from orca.common import config, logger
from orca.graph import graph
from orca.topology import utils
from orca.topology.gc import collector, remover

CONFIG = config.CONFIG
LOG = logger.get_logger(__name__)


class GarabageCollectorService(cotyledon.Service):

    """Triggers garbage collection at equal time intervals."""

    def __init__(self, worker_id, graph_lock):
        super().__init__(worker_id)
        self._graph_lock = graph_lock
        self.__graph = None

    @property
    def _graph(self):
        if not self.__graph:
            self.__graph = graph.Graph.get(self._graph_lock)
        return self.__graph

    def run(self):
        garbage_collectors = [
            collector.StaleNodeCollector(self._graph, utils.NodeSpec("elastalert", "alert"), 300),
            collector.StaleNodeCollector(self._graph, utils.NodeSpec("falco", "alert"), 300),
        ]

        garbage_remover = remover.Remover(self._graph, garbage_collectors)

        gc_interval = CONFIG.topology.gc.interval

        while True:
            start_time = time.time()
            removed_nodes = garbage_remover.run()
            gc_time = time.time() - start_time
            LOG.info("Garbage collected %i nodes (%.2f seconds)", len(removed_nodes), gc_time)
            time.sleep(gc_interval)
