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

import abc
import re

from orca import exceptions
from orca.common import config, file_utils, logger
from orca.graph import graph
from orca.topology import extractor

CONFIG = config.CONFIG
LOG = logger.get_logger(__name__)


class Extractor(extractor.Extractor):

    """Base class for alert extractors."""

    def __init__(self, source_mapper):
        super().__init__()
        self._source_mapper = source_mapper

    @property
    def kind(self):
        return 'alert'

    def extract(self, entity):
        name = self._extract_name(entity)
        labels = self._extract_source_labels(entity)
        source_mapping = self._source_mapper.map(name, labels)
        node_id = self._build_id(name, source_mapping)
        properties = self._extract_properties(entity)
        properties['name'] = name
        properties['source_mapping'] = source_mapping
        return graph.Node(node_id, properties, self.origin, self.kind)

    @abc.abstractmethod
    def _extract_name(self, entity):
        """Extract name from given entity object."""

    @abc.abstractmethod
    def _extract_source_labels(self, entity):
        """Extract labels from given entity object."""

    @abc.abstractmethod
    def _extract_properties(self, entity):
        """Extract properties from given entity object."""

    def _build_id(self, name, source_mapping):
        id_parts = [self.origin, self.kind, name]
        if source_mapping:
            id_parts.append(source_mapping['kind'])
            source_properties = source_mapping['properties']
            for key in sorted(source_properties.keys()):
                id_parts.append(source_properties[key])
        node_id = "-".join(id_parts).replace(" ", "-").lower()
        return node_id

    @classmethod
    def get(cls, origin):
        source_mapper = SourceMapper(origin)
        return cls(source_mapper)


class SourceMapper(object):

    """Retrieves source mapping for given alert entities."""

    def __init__(self, mapping_key):
        self._mapping_key = mapping_key
        self.__mapping = None

    @property
    def _mapping(self):
        if not self.__mapping:
            self.__mapping = self._load_mapping()
        return self.__mapping

    def map(self, name, labels):
        mapping = self._get_mapping(name)
        if not mapping:
            raise exceptions.MappingNotFound(key=name)
        origin = mapping['origin']
        kind = mapping['kind']
        properties = {}
        for prop, prop_mapping in mapping['properties'].items():
            value = labels.get(prop_mapping)
            valid = self._validate_value(value, mapping)
            if not valid:
                raise exceptions.InvalidMappedValue(key=name, value=value)
            properties[prop] = value
        return {'origin': origin, 'kind': kind, 'properties': properties}

    def _get_mapping(self, name):
        try:
            mapping = self._mapping['plain'].get(name)
        except:
            key = [regex for regex in self._mapping['regex'].keys() if re.match(regex, name)][0]
            mapping = self._mapping['regex'].get(key)
        return mapping

    def _load_mapping(self):
        mapping_spec = self._load_mapping_spec()
        if not mapping_spec:
            raise exceptions.MappingNotFound(key=self._mapping_key)
        blacklist_values = mapping_spec.get('blacklist_values')
        if not blacklist_values:
            blacklist_values = []
        mappings = mapping_spec['mappings']
        lookup = {}
        lookup['plain'] = {}
        lookup['regex'] = {}
        for mapping in mappings:
            name = mapping['name']
            if mapping['type'] == 'plain':
                lookup['plain'][name] = mapping['source_mapping']
                lookup['plain'][name].setdefault('blacklist_values', blacklist_values)
            else:
                lookup['regex'][name] = mapping['source_mapping']
                lookup['regex'][name].setdefault('blacklist_values', blacklist_values)
        return lookup

    def _load_mapping_spec(self):
        mapping_path = CONFIG.topology.alerts.mapping_path
        return file_utils.load_yaml(mapping_path).get(self._mapping_key)

    def _validate_value(self, value, mapping):
        if not value:
            return False
        if value in mapping['blacklist_values']:
            return False
        return True
