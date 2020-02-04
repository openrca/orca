import time

from orca.graph import graph
from orca.topology import probe


class Probe(probe.Probe):

    def run(self):
        while True:
            alert_nodes = self._graph.get_nodes(kind=self._kind)
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
