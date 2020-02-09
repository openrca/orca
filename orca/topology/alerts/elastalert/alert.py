from orca.common import str_utils
from orca.topology.alerts import extractor, probe


class AlertHandler(probe.EntityHandler):

    @staticmethod
    def create(graph):
        source_mapper = extractor.SourceMapper('elastalert')
        return AlertHandler(graph, AlertExtractor(source_mapper))


class AlertExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'es_alert'

    def _extract_name(self, entity):
        return entity['name']

    def _extract_source_labels(self, entity):
        labels = entity['kubernetes'].copy()
        labels.pop('labels', None)
        labels.pop('annotations', None)
        return labels

    def _extract_properties(self, entity):
        properties = {}
        properties['status'] = 'active'
        properties['severity'] = entity['severity']
        properties['message'] = str_utils.escape(entity['message'])
        return properties
