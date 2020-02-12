import time

from orca.topology import probe
from orca.graph import graph


class Probe(probe.Probe):

    def __init__(self, kind, graph, kiali_client):
        super().__init__(kind, graph)
        self._kiali_client = kiali_client

    def run(self):
        while True:
            self._synchronize_service_graph()
            time.sleep(60)

    def _synchronize_service_graph(self):
        namespaces = self._get_namespaces()
        nodes, edges = self._get_service_graph(namespaces)
        service_mapping = self._build_service_mapping(nodes)
        self._synchronize_links(edges, service_mapping)

    def _get_namespaces(self):
        return [namespace['name'] for namespace in self._kiali_client.list_namespaces()]

    def _get_service_graph(self, namespaces):
        service_graph = self._kiali_client.graph_namespaces(namespaces)
        node_elements = service_graph['elements']['nodes']
        edge_elements = service_graph['elements']['edges']
        nodes = [element['data'] for element in node_elements]
        edges = [element['data'] for element in edge_elements]
        return (nodes, edges)

    def _build_service_mapping(self, nodes):
        service_mapping = {}
        for node in nodes:
            if node['nodeType'] == 'service':
                service_mapping[node['id']] = {
                    'name': node['service'],
                    'namespace': node['namespace']}
        return service_mapping

    def _synchronize_links(self, edges, service_mapping):
        for edge in edges:
            source_id = edge['source']
            target_id = edge['target']
            source_mapping = service_mapping.get(source_id)
            target_mapping = service_mapping.get(target_id)
            if source_mapping and target_mapping:
                source_node = self._get_service(source_mapping)
                target_node = self._get_service(target_mapping)
                if source_node and target_node:
                    self._link_services(source_node, target_node)

    def _get_service(self, mapping):
        matches = self._graph.get_nodes('service', properties=mapping)
        if matches:
            return matches[0]

    def _link_services(self, source_node, target_node):
        link = graph.Graph.create_link({}, source_node, target_node)
        if self._graph.get_link(link.id):
            self._graph.update_link(link)
        else:
            self._graph.add_link(link)
