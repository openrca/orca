import json

from flask import request
from flask_restplus import Namespace, Resource

from orca import exceptions
from orca.common import logger
from orca.topology.alerts import probe as alert_probe
from orca.topology.alerts import extractor as alert_extractor
from orca.topology.alerts.elastalert import alert as es_alert
from orca.topology.alerts.falco import alert as falco_alert
from orca.topology.alerts.prometheus import alert as prom_alert

log = logger.get_logger(__name__)


class Ingestor(Resource):

    """Base class for alert ingestors."""

    def __init__(self, api, entity_handler):
        super().__init__()
        self._entity_handler = entity_handler

    def post(self):
        payload = request.json
        log.debug(json.dumps(payload))
        self._ingest(payload)

    def _ingest(self, entity):
        try:
            self._entity_handler.handle(entity)
        except exceptions.OrcaError as ex:
            log.warning("Error while processing an entity: %s", ex)


class Prometheus(Ingestor):

    """Prometheus ingest endpoint."""

    def post(self):
        payload = request.json
        log.debug(json.dumps(payload))
        for alert in payload['alerts']:
            self._ingest(alert)


class Falco(Ingestor):

    """Falco ingest endpoint."""


class Elastalert(Ingestor):

    """Elastalert ingest endpoint."""


def initialize(graph):
    api = Namespace('ingestor', description='Ingestor API')
    initialize_prometheus(api, graph)
    initialize_falco(api, graph)
    initialize_elastalert(api, graph)
    return api


def initialize_prometheus(api, graph):
    source_mapper = alert_extractor.SourceMapper('prometheus')
    extractor = prom_alert.AlertExtractor(source_mapper)
    entity_handler = alert_probe.EntityHandler(graph, extractor)
    api.add_resource(Prometheus, '/prometheus', resource_class_args=[entity_handler])


def initialize_falco(api, graph):
    source_mapper = alert_extractor.SourceMapper('falco')
    extractor = falco_alert.AlertExtractor(source_mapper)
    entity_handler = alert_probe.EntityHandler(graph, extractor)
    api.add_resource(Falco, '/falco', resource_class_args=[entity_handler])


def initialize_elastalert(api, graph):
    source_mapper = alert_extractor.SourceMapper('elastalert')
    extractor = es_alert.AlertExtractor(source_mapper)
    entity_handler = alert_probe.EntityHandler(graph, extractor)
    api.add_resource(Elastalert, '/elastalert', resource_class_args=[entity_handler])
