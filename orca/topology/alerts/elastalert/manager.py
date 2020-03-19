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

from orca.topology import ingestor, utils
from orca.topology.alerts import extractor, linker
from orca.topology.alerts.elastalert import extractor as es_extractor


def initialize_probes(graph):
    return []


def initialize_linkers(graph):
    return [
        linker.Linker(
            source_spec=utils.NodeSpec(origin='elastalert', kind='alert'),
            target_spec=utils.NodeSpec(origin='any', kind='any'),
            graph=graph,
            matcher=linker.AlertToSourceMatcher(),
            bidirectional=False
        )
    ]


def initialize_handler(graph):
    source_mapper = extractor.SourceMapper('elastalert')
    return ingestor.EntityHandler(graph, es_extractor.AlertExtractor(source_mapper))
