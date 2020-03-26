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

from orca.common import config
from orca.topology import probe
from orca.topology.alerts.prometheus import manager as prom
from orca.topology.infra.istio import manager as istio
from orca.topology.infra.k8s import manager as k8s
from orca.topology.infra.kiali import manager as kiali

CONFIG = config.CONFIG


class Manager(cotyledon.ServiceManager):

    """Initializes probe runners."""

    def initialize(self):
        graph_lock = multiprocessing.Lock()
        probe_managers = [k8s, istio, prom, kiali]
        for probe_manager in probe_managers:
            for probe_bundle in probe_manager.get_bundles():
                self.add(probe.ProbeRunner, workers=1, args=(probe_bundle, graph_lock))
