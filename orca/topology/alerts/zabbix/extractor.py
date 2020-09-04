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

from orca.common import str_utils
from orca.topology.alerts import extractor
from orca.topology.alerts import properties as alert_props


class Extractor(extractor.Extractor):

    """Base class for Zabbix extractors."""

    @property
    def origin(self):
        return 'zabbix'

    @classmethod
    def get(cls):
        return super().get('zabbix')


class AlertExtractor(Extractor):

    """Extractor for Alert entities retrieved from Zabbix API."""

    def _extract_name(self, entity):
        return entity['trigger'][0]

    def _extract_status(self, entity):
        if entity['trigger'][2] == '1':
            return alert_props.AlertStatus.UP
        return alert_props.AlertStatus.DOWN

    def _extract_source_labels(self, entity):
        return {'node': entity['host']}

    def _extract_properties(self, entity):
        properties = {}
        properties['severity'] = self._extract_severity(entity)
        return properties

    def _extract_severity(self, entity):
        return entity['trigger'][1]
