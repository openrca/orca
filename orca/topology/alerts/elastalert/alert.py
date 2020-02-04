from orca.common import str_utils
from orca.topology.alerts import extractor


class AlertExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'es_alert'

    def extract_name(self, entity):
        return entity['name']

    def extract_labels(self, entity):
        labels = entity['kubernetes'].copy()
        labels.pop('labels', None)
        labels.pop('annotations', None)
        return labels

    def extract_properties(self, entity):
        properties = {}
        properties['status'] = 'active'
        properties['severity'] = entity['severity']
        properties['message'] = str_utils.escape(entity['message'])
        properties['log'] = str_utils.escape(entity['log'])
        return properties
