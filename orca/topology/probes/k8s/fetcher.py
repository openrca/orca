from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher


class Fetcher(fetcher.Fetcher):

    def __init__(self, resource_api):
        super().__init__()
        self._resource_api = resource_api

    def fetch_all(self):
        self._resource_api.fetch_all()


class FetcherFactory(object):

    @staticmethod
    def get_fetcher(client, resource_kind):
        resource_api = k8s_client.ResourceAPIFactory.get_resource_api(
            client, resource_kind)
        return Fetcher(resource_api)
