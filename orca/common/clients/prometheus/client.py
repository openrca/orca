import requests

from urllib import parse as url_parse

from orca.common.clients.prometheus import exceptions
from orca.common.clients import utils as client_utils


class PrometheusClient(object):

    def __init__(self, connector):
        self._connector = connector

    def alerts(self):
        return self._connector.get("alerts")

    def instant_query(self, query):
        return self._connector.get("query", query=query)

    @staticmethod
    def get(url, **options):
        connector = PrometheusConnector(url, **options)
        return PrometheusClient(connector)


class PrometheusConnector(object):

    def __init__(self, url="http://localhost:9090", api_prefix="/api/v1", timeout=5):
        self._base_url = client_utils.join_url_paths(url, api_prefix)
        self._timeout = timeout

    def get(self, path, **params):
        url = client_utils.join_url_paths(self._base_url, path)
        try:
            response = requests.get(url, params=params, timeout=self._timeout)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as ex:
            raise exceptions.PrometheusClientException(reason=str(ex))
        return data

