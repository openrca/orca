from orca.common import str_utils
from orca.topology.alerts import extractor, probe


class AlertHandler(probe.EntityHandler):

    @staticmethod
    def create(graph):
        source_mapper = extractor.SourceMapper('falco')
        return AlertHandler(graph, AlertExtractor('falco', 'alert', source_mapper))


class AlertExtractor(extractor.Extractor):

    def _extract_origin(self, entity):
        return 'falco'

    def _extract_kind(self, entity):
        return 'alert'

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
