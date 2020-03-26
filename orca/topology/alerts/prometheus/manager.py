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

from orca.common import config
from orca.topology import ingestor
from orca.topology.alerts import extractor
from orca.topology.alerts.prometheus import extractor as prom_extractor
from orca.topology.alerts.prometheus import probe, linker

CONFIG = config.CONFIG


def initialize_probes(graph):
    return [probe.AlertProbe.get(graph)]


def initialize_linkers(graph):
    return [linker.AlertLinker.get(graph)]


def initialize_handler(graph):
    source_mapper = extractor.SourceMapper('prometheus')
    return ingestor.EventHandler(graph, prom_extractor.AlertEventExtractor(source_mapper))
