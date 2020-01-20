import abc

from orca.k8s import client as k8s_client
from orca.topology.probes import probe


class Probe(probe.Probe):

    def __init__(self, probe_id, graph, client):
        super().__init__(probe_id)
        self._graph = graph
        self._client = client


class KubeHandler(k8s_client.EventHandler, abc.ABC):

    def __init__(self, graph, extractor):
        self._graph = graph
        self._extractor = extractor

    def on_added(self, obj):
        node = self._extractor.extract(obj)
        self._graph.add_node(node)

    def on_updated(self, obj):
        node = self._extractor.extract(obj)
        self._graph.update_node(node)

    def on_deleted(self, obj):
        node = self._extractor.extract(obj)
        self._graph.delete_node(node)
