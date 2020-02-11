import time

from orca.topology import probe
from orca.graph import graph
from orca.common import logger

log = logger.get_logger(__name__)


class Probe(probe.Probe):

    def __init__(self, kind, graph, kiali_client):
        super().__init__(kind, graph)
        self._kiali_client = kiali_client

    def run(self):
        while True:
            self._update_service_links()
            time.sleep(10)

    def _update_service_links(self):
        namespaces = self._get_namespaces()
        service_graph = self._kiali_client.graph_namespaces(namespaces)

        node_elements = service_graph['elements']['nodes']
        edge_elements = service_graph['elements']['edges']

        service_mapping = {}
        for element in node_elements:
            node = element['data']
            if node['nodeType'] == 'service':
                service_mapping[node['id']] = {
                    'name': node['service'],
                    'namespace': node['namespace']}

        for element in edge_elements:
            edge = element['data']
            source_id = edge['source']
            target_id = edge['target']

            source_mapping = service_mapping.get(source_id)
            target_mapping = service_mapping.get(target_id)

            if source_mapping and target_mapping:
                self._link_services(source_mapping, target_mapping)

    def _link_services(self, source_mapping, target_mapping):
        source_matches = self._graph.get_nodes('service', properties=source_mapping)
        target_matches = self._graph.get_nodes('service', properties=target_mapping)

        if source_matches and target_matches:
            source_node = source_matches[0]
            target_node = target_matches[0]

            link = graph.Graph.create_link({}, source_node, target_node)
            log.info(link)
            self._graph.add_link(link)

    def _get_namespaces(self):
        return [namespace['name'] for namespace in self._kiali_client.list_namespaces()]
