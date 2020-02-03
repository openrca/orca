import json

from flask import request
from flask_restplus import Namespace, Resource

from orca import exceptions
from orca.common import logger
from orca.topology.alerts import extractor
from orca.topology.alerts.falco import alert as falco_alert
from orca.topology.alerts.prometheus import alert as prom_alert

log = logger.get_logger(__name__)


class IngestEndpoint(Resource):

    def __init__(self, api, graph):
        super().__init__()
        self._graph = graph


class Prometheus(IngestEndpoint):

    """Prometheus ingest endpoint."""

    def post(self):
        payload = request.json
        log.info(json.dumps(payload))
        source_mapper = extractor.SourceMapper('prometheus')
        prom_extractor = prom_alert.AlertExtractor(source_mapper)
        for alert in payload['alerts']:
            try:
                node = prom_extractor.extract(alert)
                self._graph.add_node(node)
            except exceptions.MappingNotFound as ex:
                log.warning("Mapping not found: %s", ex)
            except exceptions.InvalidMappingValue as ex:
                log.warning("Failed extracting Prometheus event: %s", ex)


class Falco(IngestEndpoint):

    """Falco ingest endpoint."""

    def post(self):
        payload = request.json
        log.debug(json.dumps(payload))
        source_mapper = extractor.SourceMapper('falco')
        falco_extractor = falco_alert.AlertExtractor(source_mapper)
        try:
            node = falco_extractor.extract(payload)
            self._graph.add_node(node)
        except exceptions.MappingNotFound as ex:
            log.warning("Mapping not found: %s", ex)
        except exceptions.InvalidMappingValue as ex:
            log.warning("Failed extracting Falco event: %s", ex)


class Elastalert(IngestEndpoint):

    """Elastalert ingest endpoint."""

    def post(self):
        payload = request.json
        log.debug(json.dumps(payload))


def initialize(graph):
    api = Namespace('ingestor', description='Ingestor API')
    api.add_resource(Prometheus, '/prometheus', resource_class_args=[graph])
    api.add_resource(Falco, '/falco', resource_class_args=[graph])
    api.add_resource(Elastalert, '/elastalert', resource_class_args=[graph])
    return api
