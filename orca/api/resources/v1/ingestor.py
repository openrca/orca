import json

from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields

from orca.common import logger

log = logger.get_logger(__name__)

api = Namespace('ingestor', description='Ingestor API')


@api.route('/prometheus')
class Prometheus(Resource):

    def post(self):
        """Ingest Prometheus alert."""
        payload = request.json
        log.info(json.dumps(payload))


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
