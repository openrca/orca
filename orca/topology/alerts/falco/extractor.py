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

from orca.common import str_utils, utils
from orca.topology.alerts import extractor
from orca.topology.alerts import properties as alert_props


class Extractor(extractor.Extractor):

    """Base class for Falco extractors."""

    @property
    def origin(self):
        return 'falco'

    @classmethod
    def get(cls):
        return super().get('falco')


class AlertExtractor(Extractor):

    """Extractor for Alert entities."""

    def _extract_name(self, entity):
        return entity['rule']

    def _extract_status(self, entity):
        # TODO: Differentiate UP/DOWN status
        return alert_props.AlertStatus.UP

    def _extract_activation_time(self, entity):
        # TODO: Extract activation time from alert payload
        return utils.get_utc()

    def _extract_source_labels(self, entity):
        return utils.flatten_dict(entity['output_fields'], sep=".")

    def _extract_properties(self, entity):
        properties = {}
        properties['status'] = 'active'
        properties['severity'] = entity['priority']
        properties['message'] = str_utils.escape(entity['output'])
        return properties
