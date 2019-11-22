from orca.topology.probes import indexer


class K8SIndexer(indexer.Indexer):

    def __init__(self, resource_api):
        super().__init__()
        self._resource_api = resource_api

    def get_all(self):
        resources = self._resource_api.get_all()
        return [K8SResourceProxy(resource) for resource in resources]

    def get_by_node(self, node):
        name = node.metadata['name']
        namespace = node.metadata.get('namespace')
        resource = self._resource_api.get(name, namespace)
        if resource:
            return K8SResourceProxy(resource)


class K8SResourceProxy(indexer.ResourceProxy):

    def get_id(self):
        return self._resource.metadata.uid
