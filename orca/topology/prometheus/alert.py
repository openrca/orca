from orca.common import str_utils
from orca.topology import extractor


class AlertExtractor(extractor.AlertExtractor):

    def extract_kind(self, entity):
        return 'prom_alert'

    def extract_name(self, entity):
        return entity['labels']['alertname']

    def extract_labels(self, entity):
        return entity['labels']

    def extract_properties(self, entity):
        properties = {}
        properties['status'] = entity['status']
        properties['severity'] = entity['labels']['severity']
        properties['message'] = str_utils.escape(entity['annotations']['message'])
        return properties
