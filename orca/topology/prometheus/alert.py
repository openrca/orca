import abc
import uuid

import yaml

from orca.topology import extractor
from orca.common import logger

log = logger.get_logger(__name__)


class AlertExtractor(extractor.AlertExtractor):

    def __init__(self):
        self._alert_mappings = self._load_alert_mappings()
        log.info(self._alert_mappings)

    def extract_id(self, entity):
        return uuid.uuid4().hex

    def extract_kind(self, entity):
        return 'prom_alert'

    def extract_name(self, entity):
        return entity['labels']['alertname']

    def extract_source_mapping(self, entity):
        alert_name = self.extract_name(entity)
        alert_props = entity['labels']

        alert_mapping = self._alert_mappings.get(alert_name)
        if not alert_mapping:
            log.warning("No alert mapping for alert: %s", alert_name)
            return {}

        kind = alert_mapping['kind']

        properties = {}
        for prop, value in alert_mapping['properties'].items():
            properties[prop] = alert_props.get(value)

        return {
            'kind': kind,
            'properties': properties}

    def extract_status(self, entity):
        return entity['status']

    def extract_severity(self, entity):
        return entity['labels']['severity']

    def extract_message(self, entity):
        return entity['annotations']['message']

    def _load_alert_mappings(self):
        with open("/etc/orca/alerts-mapping.yaml", 'r') as stream:
            prom_mappings = yaml.load(stream)['prometheus']
            return {mapping['name']:mapping['source_mapping'] for mapping in prom_mappings}
