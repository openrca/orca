import abc
import uuid

import yaml

from orca.common import logger, str_utils
from orca.graph import graph
from orca.topology import extractor

log = logger.get_logger(__name__)


class AlertExtractor(extractor.Extractor):

    def __init__(self):
        self._source_mappings = self._load_source_mappings()
        log.info(self._source_mappings)

    def extract(self, entity):
        kind = 'prom_alert'
        name = entity['labels']['alertname']
        source_mapping = self._extract_source_mapping(name, entity)
        node_id = self._build_id(kind, name, source_mapping)
        properties = {}
        properties['name'] = name
        properties['status'] = entity['status']
        properties['severity'] = entity['labels']['severity']
        properties['message'] = str_utils.escape(entity['annotations']['message'])
        properties['source_mapping'] = source_mapping
        return graph.Node(node_id, properties, kind)

    def _build_id(self, kind, name, source_mapping):
        id_parts = [kind, name]
        if source_mapping:
            id_parts.append(source_mapping['kind'])
            source_properties = source_mapping['properties']
            for key in sorted(source_properties.keys()):
                id_parts.append(source_properties[key])
        node_id = "-".join(id_parts)
        return node_id

    def _extract_source_mapping(self, name, entity):
        source_mapping = self._source_mappings.get(name)
        if not source_mapping:
            log.warning("No source mapping for alert: %s", name)
            return

        alert_labels = entity['labels']
        source_kind = source_mapping['kind']
        source_properties = {}
        for prop, value in source_mapping['properties'].items():
            source_properties[prop] = alert_labels.get(value)

        return {
            'kind': source_kind,
            'properties': source_properties}

    def _load_source_mappings(self):
        with open("/etc/orca/alerts-mapping.yaml", 'r') as stream:
            prom_mappings = yaml.load(stream)['prometheus']
            return {mapping['name']: mapping['source_mapping'] for mapping in prom_mappings}
