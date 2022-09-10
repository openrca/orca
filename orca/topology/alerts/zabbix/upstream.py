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

from orca.topology import upstream
from orca.common import config

CONFIG = config.CONFIG


class UpstreamProxy(upstream.UpstreamProxy):

    """Upstream proxy for Zabbix."""

    def __init__(self, client):
        self._client = client
        self._client.login(CONFIG.probes.zabbix.username, CONFIG.probes.zabbix.password)

    def get_all(self):
        all = self._client.trigger.get(
            only_true=1,
            active=1,
            output='extend',
            selectHosts=['host'])
        triggers = []
        for trigger in all:
            for host in trigger['hosts']:
                payload = {}
                payload['host'] = host['host']
                payload['trigger'] = [
                    trigger.pop(property) for property in ['description', 'priority', 'value']]
                triggers.append(payload)
        return triggers

    def get_events(self):
        raise NotImplementedError()
