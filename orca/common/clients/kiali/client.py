from urllib import parse as url_parse

import requests
from requests import auth

from orca.common.clients import utils as client_utils
from orca.common.clients.kiali import exceptions


class KialiClient(object):

    def __init__(self, connector):
        self._connector = connector

    def graph_namespace(self, namespace):
        return self._connector.get("/namespaces/graph", namespaces=namespace, graphType='service')

    @staticmethod
    def get(url, username=None, password=None):
        basic_auth = None
        if username and password:
            basic_auth = auth.HTTPBasicAuth(username, password)
        connector = KialiConnector(url, auth=basic_auth)
        return KialiClient(connector)


class KialiConnector(object):

    def __init__(self, url="http://localhost:20001", api_prefix="/kiali/api", auth=None, timeout=5):
        self._base_url = client_utils.join_url_paths(url, api_prefix)
        self._auth = auth
        self._timeout = timeout

    def get(self, path, **params):
        url = client_utils.join_url_paths(self._base_url, path)

        try:
            response = requests.get(url, params=params, auth=self._auth, timeout=self._timeout)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as ex:
            raise exceptions.KialiClientException(reason=str(ex))
        return data
