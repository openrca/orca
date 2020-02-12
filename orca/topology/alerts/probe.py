import time

from orca.common import logger
from orca.graph import graph
from orca.topology import probe

log = logger.get_logger(__name__)


class Probe(probe.Probe):

    def __init__(self, origin, kind, graph):
        super().__init__(kind, graph)
        self._origin = origin

    def run(self):
        while True:
            alert_nodes = self._graph.get_nodes(origin=self._origin, kind=self._kind)
            for alert_node in alert_nodes:
                source_mapping = alert_node.properties.source_mapping
                if not source_mapping:
                    continue
                source_nodes = self._graph.get_nodes(
                    kind=source_mapping.kind, properties=source_mapping.properties)
                for source_node in source_nodes:
                    link = graph.Graph.create_link({}, source_node, alert_node)
                    self._graph.add_link(link)
            time.sleep(10)


class EntityHandler(object):

    def __init__(self, graph, extractor):
        self._graph = graph
        self._extractor = extractor

    def handle(self, entity):
        node = self._extractor.extract(entity)
        self._graph.add_node(node)
