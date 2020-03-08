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
from orca.topology.alerts import extractor, probe


class AlertHandler(probe.EntityHandler):

    @staticmethod
    def create(graph):
        source_mapper = extractor.SourceMapper('falco')
        return AlertHandler(graph, AlertExtractor(source_mapper))


class AlertExtractor(extractor.Extractor):

    def get_origin(self):
        return 'falco'

    def _extract_name(self, entity):
        return entity['rule']

    def _extract_source_labels(self, entity):
        return entity['output_fields']

    def _extract_properties(self, entity):
        properties = {}
        properties['status'] = 'active'
        properties['severity'] = entity['priority']
        properties['message'] = str_utils.escape(entity['output'])
        return properties
