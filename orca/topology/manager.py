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

import multiprocessing

import cotyledon

from orca.topology import probe
from orca.topology.alerts import prometheus
from orca.topology.infra import istio
from orca.topology.infra import k8s
from orca.topology.infra import kiali


class Manager(cotyledon.ServiceManager):

    """Initializes probe runners."""

    def initialize(self):
        graph_lock = multiprocessing.Lock()
        probe_modules = [k8s, istio, kiali, prometheus]
        for probe_module in probe_modules:
            for probe_bundle in probe_module.get_probes():
                self.add(probe.ProbeRunner, workers=1, args=(probe_bundle, graph_lock))
