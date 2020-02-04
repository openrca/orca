import json

from flask import request
from flask_restplus import Namespace, Resource

from orca import exceptions
from orca.common import logger
from orca.topology.alerts.elastalert import alert as elastalert
from orca.topology.alerts.falco import alert as falco
from orca.topology.alerts.prometheus import alert as prometheus

log = logger.get_logger(__name__)


class Ingestor(Resource):

    """Base class for alert ingestors."""

    def __init__(self, api, entity_handler):
        super().__init__()
        self._entity_handler = entity_handler

    def post(self):
        payload = request.json
        log.debug("Ingested an entity: %s", json.dumps(payload))
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
    api.add_resource(
        Prometheus, '/prometheus',
        resource_class_args=[prometheus.AlertHandler.create(graph)])
    api.add_resource(
        Falco, '/falco',
        resource_class_args=[falco.AlertHandler.create(graph)])
    api.add_resource(
        Elastalert, '/elastalert',
        resource_class_args=[elastalert.AlertHandler.create(graph)])
    return api
