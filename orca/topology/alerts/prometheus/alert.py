from orca.common import str_utils
from orca.topology.alerts import extractor, probe


class AlertProbe(probe.Probe):

    @staticmethod
    def create(graph):
        return AlertProbe('prom_alert', graph)


class AlertExtractor(extractor.Extractor):

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
