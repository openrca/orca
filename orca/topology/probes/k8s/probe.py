from abc import ABC, abstractmethod

from orca.topology.probes import probe
from orca.k8s import client as k8s_client
from orca import graph


class K8SProbe(probe.Probe):

    def __init__(self, probe_id, graph, client):
        super().__init__(probe_id)
        self._graph = graph
        self._client = client


class K8SHandler(k8s_client.EventHandler, ABC):

    def __init__(self, graph):
        self._graph = graph

    def on_added(self, obj):
        (id, metadata) = self._extract_properties(obj)
        node = graph.Graph.create_node(id, metadata)
        self._graph.add_node(node)

    def on_updated(self, obj):
        (id, metadata) = self._extract_properties(obj)
        node = graph.Graph.create_node(id, metadata)
        self._graph.update_node(node)

    def on_deleted(self, obj):
        (id, metadata) = self._extract_properties(obj)
        node = graph.Graph.create_node(id, metadata)
        self._graph.delete_node(node)

    @abstractmethod
    def _extract_properties(self, obj):
        """Extracts properties from K8S resource object."""
