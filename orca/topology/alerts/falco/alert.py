from orca.common import str_utils
from orca.topology.alerts import extractor


class AlertExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'falco_alert'

    def extract_name(self, entity):
        return entity['rule']

    def extract_labels(self, entity):
        return entity['output_fields']

    def extract_properties(self, entity):
        properties = {}
        properties['status'] = 'active'
        properties['severity'] = entity['priority']
        properties['message'] = str_utils.escape(entity['output'])
        return properties
