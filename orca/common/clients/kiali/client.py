from requests import auth

from orca.common.clients import client


class KialiClient(client.APIClient):

    def __init__(self, connector):
        self._connector = connector

    def list_namespaces(self):
        return self._connector.get("/namespaces")

    def graph_namespaces(self, namespaces, graph_type='service'):
        namespace_list = ','.join(namespaces)
        return self._connector.get(
            "/namespaces/graph", namespaces=namespace_list, graphType=graph_type)

    @staticmethod
    def get(url="http://localhost:20001", api_prefix="/kiali/api", username=None, password=None):
        basic_auth = None
        if username and password:
            basic_auth = auth.HTTPBasicAuth(username, password)
        connector = client.APIConnector(url, api_prefix=api_prefix, auth=basic_auth)
        return KialiClient(connector)
