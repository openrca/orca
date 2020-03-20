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
from orca.common.clients.kiali import client as kiali
from orca.topology.infra.kiali import probe

CONFIG = config.CONFIG


def initialize_probes(graph):
    kiali_client = kiali.KialiClient.get(
        url=CONFIG.kiali.url,
        username=CONFIG.kiali.username,
        password=CONFIG.kiali.password)
    return [probe.Probe(graph=graph, kiali_client=kiali_client)]


def initialize_linkers(graph):
    return []
