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

from orca.common.clients.prometheus import client as prometheus
from orca.topology import probe, synchronizer
from orca.topology.alerts import extractor, linker
from orca.topology.alerts.prometheus import extractor as prom_extractor
from orca.topology.alerts.prometheus import probe as prom_probe


def initialize_probes(graph):
    source_mapper = extractor.SourceMapper('prometheus')
    prom_client = prometheus.PrometheusClient.get(
        "http://prometheus-prometheus-oper-prometheus.monitoring:9090")
    return [
        probe.PullProbe(
            graph=graph,
            upstream_proxy=prom_probe.UpstreamProxy(prom_client),
            extractor=prom_extractor.AlertExtractor(source_mapper),
            synchronizer=synchronizer.NodeSynchronizer(graph)
        )
    ]


def initialize_linkers(graph):
    linkers = []
    for kind in ('pod', 'daemon_set', 'persistent_volume', 'horizontal_pod_autoscaler', 'node'):
        linkers.append(
            linker.Linker(
                source_kind='alert',
                target_kind=kind,
                graph=graph,
                matcher=linker.AlertToSourceObjectMatcher(),
                bidirectional=False
            ))
    return linkers
