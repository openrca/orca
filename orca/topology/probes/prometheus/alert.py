import abc
import uuid

from orca.topology.probes import extractor


class Extractor(extractor.AlertExtractor):

    def extract_id(self, entity):
        return uuid.uuid4().hex

    def extract_kind(self, entity):
        return 'prom_alert'

    def extract_name(self, entity):
        return entity['labels']['alertname']

    def extract_source_labels(self, entity):
        return entity['labels'].copy()

    def extract_status(self, entity):
        return entity['status']

    def extract_severity(self, entity):
        return entity['labels']['severity']

    def extract_message(self, entity):
        return entity['annotations']['message']
