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

from pyzabbix import ZabbixAPI
from orca.common import config
from orca.topology import probe, utils
from orca.topology.alerts.zabbix import extractor, upstream

CONFIG = config.CONFIG


class AlertProbe(probe.PullProbe):

    """Alert pull probe."""

    @classmethod
    def get(cls, graph):
        zabbix_client = ZabbixAPI(CONFIG.probes.zabbix.url)
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(zabbix_client),
            extractor=extractor.AlertExtractor.get(),
            synchronizer=utils.NodeSynchronizer(graph),
            resync_period=CONFIG.probes.zabbix.resync_period,
        )
