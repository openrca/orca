from orca import exceptions
from orca.common import file_utils, logger, str_utils
from orca.graph import graph
from orca.topology import extractor

log = logger.get_logger(__name__)


class AlertExtractor(extractor.Extractor):

    def __init__(self, source_mapper):
        super().__init__()
        self._source_mapper = source_mapper

    def extract(self, entity):
        kind = self.extract_kind(entity)
        name = self.extract_name(entity)
        labels = self.extract_labels(entity)
        source_mapping = self._source_mapper.map(name, labels)
        node_id = self._build_id(kind, name, source_mapping)
        properties = self.extract_properties(entity)
        properties['name'] = name
        properties['source_mapping'] = source_mapping
        return graph.Node(node_id, properties, kind)

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

    def _build_id(self, kind, name, source_mapping):
        id_parts = [kind, name]
        if source_mapping:
            id_parts.append(source_mapping['kind'])
            source_properties = source_mapping['properties']
            for key in sorted(source_properties.keys()):
                id_parts.append(source_properties[key])
        node_id = "-".join(id_parts).replace(" ", "-")
        return node_id


class SourceMapper(object):

    def __init__(self, mapping_key):
        self._mapping_key = mapping_key
        self.__mapping = None

    @property
    def _mapping(self):
        if not self.__mapping:
            self.__mapping = self._load_mapping()
        return self.__mapping

    def map(self, name, labels):
        mapping = self._mapping.get(name)
        if not mapping:
            log.warning("No source mapping for key: %s", name)
            return
        kind = mapping['kind']
        properties = {}
        for prop, prop_mapping in mapping['properties'].items():
            value = labels.get(prop_mapping)
            valid = self._validate_value(value, mapping)
            if not valid:
                raise exceptions.InvalidMappingValue(key=name, value=value)
            properties[prop] = value
        return {'kind': kind, 'properties': properties}

    def _load_mapping(self):
        # TODO: Read mapping path from config
        mapping_path = "/etc/orca/alerts-mapping.yaml"
        mapping_spec = file_utils.load_yaml(mapping_path).get(self._mapping_key)
        if not mapping_spec:
            raise exceptions.MappingNotFound(key=self._mapping_key)

        blacklist_values = mapping_spec.get('blacklist_values')
        if not blacklist_values:
            blacklist_values = []

        mappings = mapping_spec['mappings']
        lookup = {}
        for mapping in mappings:
            name = mapping['name']
            lookup[name] = mapping['source_mapping']
            lookup[name].setdefault('blacklist_values', blacklist_values)
        return lookup

    def _validate_value(self, value, mapping):
        if not value:
            return False
        if value in mapping['blacklist_values']:
            return False
        return True
