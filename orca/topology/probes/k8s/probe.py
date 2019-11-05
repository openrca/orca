from abc import ABC, abstractmethod

from orca.topology.probes import probe
from orca.topology.probes.k8s import client as k8s_client


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
        # TODO: use GraphObject
        # TODO: catch exceptions
        self._graph.create_node(id, metadata)

    def on_update(self, obj):
        (id, metadata) = self._extract_properties(obj)
        # TODO: use GraphObject
        # TODO: catch exceptions
        self._graph.update_node(id, metadata)

    def on_delete(self, obj):
        (id, _metadata) = self._extract_properties(obj)
        # TODO: use GraphObject
        # TODO: catch exceptions
        self._graph.delete_node(id)

    @abstractmethod
    def _extract_properties(self, obj):
        """Extracts properties from raw K8S resource object."""
