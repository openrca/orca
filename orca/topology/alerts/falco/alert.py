from orca.common import str_utils
from orca.topology.alerts import extractor, probe


class AlertHandler(probe.EntityHandler):

    @staticmethod
    def create(graph):
        source_mapper = extractor.SourceMapper('falco')
        return AlertHandler(graph, AlertExtractor(source_mapper))


class AlertExtractor(extractor.Extractor):

    def get_origin(self):
        return 'falco'

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
