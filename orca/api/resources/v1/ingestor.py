import json

from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from orca.common import logger
from orca.topology.prometheus import alert as prom_alert

log = logger.get_logger(__name__)

api = Namespace('ingestor', description='Ingestor API')


@api.route('/prometheus')
class Prometheus(Resource):

    def post(self):
        """Ingest Prometheus alert."""
        payload = request.json
        log.info(json.dumps(payload))
        extractor = prom_alert.AlertExtractor()
        for alert in payload['alerts']:
            node = extractor.extract(alert)
            log.info(node)


@api.route('/falco')
class Falco(Resource):

    def post(self):
        """Ingest Falco alert."""
        payload = request.json
        log.info(json.dumps(payload))


@api.route('/elastalert')
class Elastalert(Resource):

    def post(self):
        """Ingest Elasticsearch alert."""
        payload = request.json
        log.info(json.dumps(payload))

