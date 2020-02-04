from orca.common import str_utils
from orca.topology.alerts import extractor, probe


class AlertProbe(probe.Probe):

    @staticmethod
    def create(graph):
        return AlertProbe('falco_alert', graph)


class AlertExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'falco_alert'

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
