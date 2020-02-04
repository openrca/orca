from orca.common import str_utils
from orca.topology.alerts import extractor, probe


class AlertProbe(probe.Probe):

    @staticmethod
    def create(graph):
        return AlertProbe('prom_alert', graph)


class AlertHandler(probe.EntityHandler):

    @staticmethod
    def create(graph):
        source_mapper = extractor.SourceMapper('prometheus')
        return AlertHandler(graph, AlertExtractor(source_mapper))


class AlertExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'prom_alert'

    def _extract_name(self, entity):
        return entity['labels']['alertname']

    def _extract_source_labels(self, entity):
        return entity['labels']

    def _extract_properties(self, entity):
        properties = {}
        properties['status'] = entity['status']
        properties['severity'] = entity['labels']['severity']
        properties['message'] = str_utils.escape(entity['annotations']['message'])
        return properties
