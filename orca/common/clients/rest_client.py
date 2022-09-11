import requests
from requests import exceptions as req_exceptions

from orca.common.clients import exceptions, utils


class APIClient(object):
    def __init__(self, connector):
        self._connector = connector


class APIConnector(object):
    def __init__(self, url, api_prefix=None, auth=None, timeout=5):
        self._base_url = utils.join_url_paths(url, api_prefix)
        self._auth = auth
        self._timeout = timeout

    def get(self, path, **params):
        url = utils.join_url_paths(self._base_url, path)
        try:
            response = requests.get(
                url, params=params, auth=self._auth, timeout=self._timeout
            )
            response.raise_for_status()
            data = response.json()
        except req_exceptions.RequestException as ex:
            raise exceptions.APIClientError(reason=str(ex))
        return data
