import abc

import cotyledon


class ProbeService(cotyledon.Service):

    def __init__(self, service_id, probe):
        super().__init__(service_id)
        self._service_id = service_id
        self._probe = probe

    def run(self):
        self._probe.run()


class Probe(abc.ABC):

    def __init__(self, graph):
        super().__init__()
        self._graph = graph

    @abc.abstractmethod
    def run(self):
        """Starts entity probe."""
