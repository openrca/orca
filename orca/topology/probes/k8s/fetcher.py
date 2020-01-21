from orca.k8s import client as k8s_client
from orca.topology.probes import fetcher


class Fetcher(fetcher.Fetcher):

    def __init__(self, resource_api, extractor):
        super().__init__()
        self._resource_api = resource_api
        self._extractor = extractor

    def fetch_all(self):
        entities = self._resource_api.get_all()
        return [self._extractor.extract(entity) for entity in entities]


class FetcherFactory(object):

    @staticmethod
    def get_fetcher(client, entity_kind, extractor):
        resource_api = k8s_client.ResourceAPIFactory.get_resource_api(
            client, entity_kind)
        return Fetcher(resource_api, extractor)
