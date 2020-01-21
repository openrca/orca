from orca.k8s import client as k8s_client
from orca.topology.probes import indexer


class Indexer(indexer.Indexer):

    def __init__(self, resource_api):
        super().__init__()
        self._resource_api = resource_api

    def get_all(self):
        self._resource_api.get_all()


class IndexerFactory(object):

    @staticmethod
    def get_indexer(client, resource_kind):
        resource_api = k8s_client.ResourceAPIFactory.get_resource_api(
            client, resource_kind)
        return Indexer(resource_api)
