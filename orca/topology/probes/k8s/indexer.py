from orca.topology.probes import indexer
from orca.k8s import client as k8s_client


class Indexer(indexer.Indexer):

    def __init__(self, resource_api):
        super().__init__()
        self._resource_api = resource_api

    def get_all(self):
        resources = self._resource_api.get_all()
        return [ResourceProxy(resource) for resource in resources]

    def get_by_node(self, node):
        name = node.metadata['name']
        namespace = node.metadata.get('namespace')
        resource = self._resource_api.get(name, namespace)
        if resource:
            return ResourceProxy(resource)


class ResourceProxy(indexer.ResourceProxy):

    def get_id(self):
        return self._resource.metadata.uid


class IndexerFactory(object):

    @staticmethod
    def get_indexer(client, resource_kind):
        resource_api = k8s_client.ResourceAPIFactory.get_resource_api(
            client, resource_kind)
        return Indexer(resource_api)
