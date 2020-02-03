import json

from flask import request
from flask_restplus import Namespace, Resource

from orca import exceptions
from orca.common import logger
from orca.topology.alerts import extractor as alert_extractor
from orca.topology.alerts.falco import alert as falco_alert
from orca.topology.alerts.prometheus import alert as prom_alert

log = logger.get_logger(__name__)


class Ingestor(Resource):

    """Template class for alert ingestors."""

    def __init__(self, api, graph, extractor):
        super().__init__()
        self._graph = graph
        self._extractor = extractor

    def ingest(self, entity):
        try:
            node = self._extractor.extract(entity)
            self._graph.add_node(node)
        except (exceptions.MappingNotFound, exceptions.InvalidMappingValue) as ex:
            log.warning("Error while processing ingested entity: %s", ex)


class Prometheus(Ingestor):

    """Prometheus ingest endpoint."""

    def post(self):
        payload = request.json
        log.debug(json.dumps(payload))
        for alert in payload['alerts']:
            self.ingest(alert)


class Falco(Ingestor):

    """Falco ingest endpoint."""

    def post(self):
        payload = request.json
        log.debug(json.dumps(payload))
        self.ingest(payload)


def initialize(graph):
    api = Namespace('ingestor', description='Ingestor API')
    initialize_prometheus(api, graph)
    initialize_falco(api, graph)
    return api

def initialize_prometheus(api, graph):
    source_mapper = alert_extractor.SourceMapper('prometheus')
    extractor = prom_alert.AlertExtractor(source_mapper)
    api.add_resource(Prometheus, '/prometheus', resource_class_args=[graph, extractor])

def initialize_falco(api, graph):
    source_mapper = alert_extractor.SourceMapper('falco')
    extractor = falco_alert.AlertExtractor(source_mapper)
    api.add_resource(Falco, '/falco', resource_class_args=[graph, extractor])
